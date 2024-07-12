"""server/router/stream.py"""

import datetime
import json
import time

import pytz
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

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
