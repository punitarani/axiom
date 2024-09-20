#! /usr/bin/env python3

import asyncio
import io
import os
import tempfile

import backoff
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm.asyncio import tqdm

from axiom.config import DATA_DIR
from axiom.schwab_client import get_schwab_client, sch_limiter
from axiom.supabase import supabase

sch = get_schwab_client()


@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=3,
    base=2,
    factor=1
)
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
        
        SUPABASE_BUCKET = "daily-data"
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.parquet') as tmp_file:
            temp_path = tmp_file.name
            
            # Save DataFrame as parquet to the temporary file
            df.to_parquet(temp_path, engine='pyarrow')
        
        try:
            # Upload the temporary file to Supabase
            file_name = f"{symbol}.parquet"
            with open(temp_path, 'rb') as f:
                supabase.storage.from_(SUPABASE_BUCKET).upload(file_name, f)
        finally:
            # Delete the temporary file
            os.unlink(temp_path)

async def download_daily_dataset():
    screener_fp = DATA_DIR.joinpath("high-volume-equity-screen.csv")

    # Read the symbols from the file (limit to 1000 for now)
    symbols = pd.read_csv(screener_fp)["Ticker"].tolist()[:1000]

    # Create a semaphore to limit concurrent tasks to 25
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
