"""server/router/stream.py"""

import asyncio
import datetime
import json

import pytz
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from axiom.store.cache import level_one_cache

router = APIRouter(prefix="/stream")


@router.websocket("/clock")
async def clock(websocket: WebSocket):
    await websocket.accept()
    est = pytz.timezone("US/Eastern")
    try:
        while True:
            now = datetime.datetime.now(est).strftime("%Y-%m-%d %H:%M:%S")
            await websocket.send_text(json.dumps({"time": now}))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Client disconnected")


@router.websocket("/equity/level-one")
async def equity_level_one(websocket: WebSocket, frequency: int = 10):
    if frequency < 1 or frequency > 60:
        await websocket.close(code=4000)
        return

    await websocket.accept()
    key_error_count = 0
    try:
        while True:
            try:
                data = level_one_cache["SPY"]
                await websocket.send_text(data)
                key_error_count = 0  # Reset the count if data is found
                await asyncio.sleep(frequency)
            except KeyError:
                key_error_count += 1
                if key_error_count >= 3:
                    await websocket.close(code=5000)
                    return
                await asyncio.sleep(frequency)
    except WebSocketDisconnect:
        print("Client disconnected")
