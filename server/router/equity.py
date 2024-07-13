"""server/router/equity.py"""

from fastapi import APIRouter, HTTPException

from axiom.mdata.equity import get_daily_price_history
from axiom.schwab_models import CandleList

router = APIRouter(prefix="/equity")


@router.get("/history/daily")
async def get_history_daily_price(symbol: str = "SPY") -> CandleList:
    # Temporarily only allow SPY
    if symbol != "SPY":
        raise HTTPException(status_code=404, detail="Symbol not supported")

    return await get_daily_price_history(symbol)
