"""server/router/stream.py"""

import asyncio
import datetime
import json
import time

import pytz
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from axiom.store.cache import level_one_cache

router = APIRouter(prefix="/stream")


def generate_clock() -> str:
    est = pytz.timezone("US/Eastern")
    while True:
        now = datetime.datetime.now(est).strftime("%Y-%m-%d %H:%M:%S")
        yield json.dumps({"time": now})
        time.sleep(1)


@router.get("/clock")
async def clock():
    return StreamingResponse(generate_clock(), media_type="application/json")


@router.get("/equity/level-one")
async def equity_level_one(frequency: int = 10):
    if frequency < 1 or frequency > 60:
        raise HTTPException(status_code=400, detail="Frequency must be between 1 and 60 seconds")

    async def generate_equity_level_one():
        key_error_count = 0
        while True:
            try:
                data = level_one_cache["SPY"]
                yield data
                key_error_count = 0  # Reset the count if data is found
                await asyncio.sleep(frequency)
            except KeyError:
                key_error_count += 1
                if key_error_count >= 3:
                    raise HTTPException(status_code=500, detail="Error fetching data")
                await asyncio.sleep(frequency)

    return StreamingResponse(generate_equity_level_one(), media_type="application/json")
