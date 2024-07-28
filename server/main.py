"""
server/main.py

FastAPI app for axiom
"""

import asyncio
import os
from asyncio import Task
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .load import load_models
from .router import auth_router, equity_router, ml_router, stream_router

MODE = os.getenv("MODE", "prod")
PORT = int(os.getenv("PORT", 8123))

stream_task: Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa (allow app to be unused)
    await load_models()
    yield


app = FastAPI(title="Axiom", lifespan=lifespan)

# Add CORS middleware
if MODE == "dev":
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:3123",
        "https://axiom.punitarani.com",
    ]
else:
    origins = [
        "https://axiom.punitarani.com",
    ]

app.add_middleware(
    CORSMiddleware,  # noinspection PyTypeChecker
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(auth_router)
app.include_router(equity_router)
app.include_router(ml_router)
app.include_router(stream_router)


@app.post("/start")
async def start_stream():
    from axiom.ws.equity_level_one import run_equity_level_one_stream

    global stream_task
    if stream_task is None or stream_task.done():
        stream_task = asyncio.create_task(run_equity_level_one_stream())
        return {"message": "Stream started"}
    else:
        raise HTTPException(status_code=400, detail="Stream is already running")


@app.post("/stop")
async def stop_stream():
    global stream_task
    if stream_task is not None and not stream_task.done():
        # Attempt to cancel the task
        stream_task.cancel()
        try:
            await stream_task
            return {"message": "Stream stopped"}
        except asyncio.CancelledError:
            return {"message": "Stream stopped successfully"}
    else:
        raise HTTPException(status_code=400, detail="Stream is not running")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="server.main:app", host="0.0.0.0", port=PORT, reload=True if MODE == "dev" else False
    )
