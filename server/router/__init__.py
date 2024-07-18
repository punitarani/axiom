"""
server.router package

FastAPI Server Routers
"""

from .equity import router as equity_router
from .ml import router as ml_router
from .stream import router as stream_router
