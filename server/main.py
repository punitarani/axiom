"""
server/main.py

FastAPI app for axiom
"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from axiom.ws.equity_level_one import run_equity_level_one_stream

from .router import equity_router, stream_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa (allow app to be unused)
    task = asyncio.create_task(run_equity_level_one_stream())
    yield
    task.cancel()
    await task


app = FastAPI(lifespan=lifespan)

# Add routers
app.include_router(equity_router)
app.include_router(stream_router)
