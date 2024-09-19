"""
server/main.py

FastAPI app for axiom
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from axiom.config import ensure_env_vars
from axiom.ws.equity_level_one import run_equity_level_one_stream

from .load import download_schwab_token, load_models
from .router import auth_router, equity_router, ml_router, stream_router

MODE = os.getenv("MODE", "prod")
PORT = int(os.getenv("PORT", 8123))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the stream task
stream_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa (allow app to be unused)
    ensure_env_vars()

    # Download the Schwab token
    if MODE == "prod":
        download_schwab_token()

    # Load the ML models
    await load_models()

    # Start the Equity Level One stream
    global stream_task
    stream_task = asyncio.create_task(run_equity_level_one_stream())

    yield

    # Cancel the Equity Level One stream
    if stream_task:
        stream_task.cancel()
        await stream_task


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

logger.info(f"Running in {MODE} mode. Allowed origins: {origins}")

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


# Function to restart the stream
async def restart_stream():
    global stream_task
    if stream_task:
        stream_task.cancel()
        await stream_task
    stream_task = asyncio.create_task(run_equity_level_one_stream())
    logger.info("Equity Level One stream restarted")


# Endpoint to manually restart the stream
@app.post("/restart-stream")
async def restart_stream_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(restart_stream)
    return {"message": "Stream restart initiated"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="server.main:app", host="0.0.0.0", port=PORT, reload=True if MODE == "dev" else False
    )
