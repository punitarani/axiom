"""
server/main.py

FastAPI app for axiom
"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from axiom.ws.equity_level_one import run_equity_level_one_stream

from .load import load_models
from .router import equity_router, ml_router, stream_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa (allow app to be unused)
    await load_models()
    task = asyncio.create_task(run_equity_level_one_stream())
    yield
    task.cancel()
    await task


app = FastAPI(title="Axiom", lifespan=lifespan)

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,  # noinspection PyTypeChecker
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routers
app.include_router(equity_router)
app.include_router(ml_router)
app.include_router(stream_router)
