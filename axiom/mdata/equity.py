"""axiom/mdata/equity.py"""

from datetime import datetime, timedelta

import pytz

from axiom.schwab_client import sch, sch_limiter
from axiom.schwab_models import CandleList
from axiom.store.cache import daily_price_history_cache


async def get_daily_price_history(symbol: str) -> CandleList:
    """Get daily price history for a given symbol."""

    # Check the cache first
    try:
        data = daily_price_history_cache[symbol]
    except KeyError:
        async with sch_limiter:
            response = await sch.get_price_history(
                symbol=symbol,
                frequency=sch.PriceHistory.Frequency.DAILY,
                frequency_type=sch.PriceHistory.FrequencyType.DAILY,
                period=sch.PriceHistory.Period.TWENTY_YEARS,
                period_type=sch.PriceHistory.PeriodType.YEAR,
            )
            data = response.json()

        # Save the response to the cache with expiration at 1am EST
        now = datetime.now(pytz.timezone("US/Eastern"))
        expire_at: datetime = now.replace(hour=1, minute=0, second=0, microsecond=0)
        if now >= expire_at:
            expire_at += timedelta(days=1)
        expire: float = (expire_at - now).total_seconds()
        daily_price_history_cache.set(symbol, data, expire=expire)

    return CandleList.model_validate(data)
