#! /usr/bin/env python3

import asyncio
import os

import backoff
import pandas as pd
from tqdm.asyncio import tqdm

from axiom.config import DATA_DIR
from axiom.schwab_client import get_schwab_client, sch_limiter

sch = get_schwab_client()


@backoff.on_exception(backoff.expo, Exception, max_tries=3, base=2, factor=1)
async def download_equity_data(symbol: str):
    async with sch_limiter:
        response = await sch.get_price_history(
            symbol=symbol,
            frequency=sch.PriceHistory.Frequency.DAILY,
            frequency_type=sch.PriceHistory.FrequencyType.DAILY,
            period=sch.PriceHistory.Period.TWENTY_YEARS,
            period_type=sch.PriceHistory.PeriodType.YEAR,
        )
        data = response.json()

        # Get a list of candles
        candles = data.get("candles", [])
        df = pd.DataFrame(candles)

        # Create the directory if it doesn't exist
        save_dir = DATA_DIR.joinpath("mdata", "daily-data")
        save_dir.mkdir(parents=True, exist_ok=True)

        # Save DataFrame as parquet
        file_path = save_dir / f"{symbol}.parquet"
        df.to_parquet(file_path, engine="pyarrow")


async def download_daily_dataset():
    screener_fp = DATA_DIR.joinpath("high-volume-equity-screen.csv")

    # Read the symbols from the file (limit to 1000 for now)
    symbols = pd.read_csv(screener_fp)["Ticker"].tolist()[:1000]

    # Create a semaphore to limit concurrent tasks to 40
    semaphore = asyncio.Semaphore(40)

    async def bounded_download_equity_data(symbol: str):
        async with semaphore:
            try:
                await download_equity_data(symbol)
                return f"Successfully downloaded {symbol}"
            except Exception as e:
                return f"Failed to download {symbol}: {str(e)}"

    # Create tasks for all symbols
    tasks = [bounded_download_equity_data(symbol) for symbol in symbols]

    # Use tqdm.gather to run tasks concurrently and collect results with a progress bar
    await tqdm.gather(*tasks, desc="Downloading data", total=len(symbols))


if __name__ == "__main__":
    import asyncio

    asyncio.run(download_daily_dataset())
