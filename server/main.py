"""
server/main.py

FastAPI app for axiom
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from axiom.ws.equity_level_one import run_equity_level_one_stream

from .load import download_schwab_token, load_models
from .router import auth_router, equity_router, ml_router, stream_router

MODE = os.getenv("MODE", "prod")
PORT = int(os.getenv("PORT", 8123))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa (allow app to be unused)
    if MODE == "prod":
        download_schwab_token()
    await load_models()
    task = asyncio.create_task(run_equity_level_one_stream())
    yield
    task.cancel()
    await task


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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="server.main:app", host="0.0.0.0", port=PORT, reload=True if MODE == "dev" else False
    )
