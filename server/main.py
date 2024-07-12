"""
server/main.py

FastAPI app for axiom
"""

from fastapi import FastAPI

from .router import stream_router

app = FastAPI()

# Add routers
app.include_router(stream_router)
