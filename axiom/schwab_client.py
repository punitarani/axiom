"""axiom/schwab_client.py"""

import os

from aiolimiter import AsyncLimiter
from schwab import auth
from schwab.client import AsyncClient

from axiom.config import DATA_DIR

SCHWAB_APP_KEY = os.environ["SCHWAB_APP_KEY"]
SCHWAB_SECRET = os.environ["SCHWAB_SECRET"]
SCHWAB_REDIRECT_URI = "https://127.0.0.1"
SCHWAB_TOKEN_FP = DATA_DIR.joinpath("schwab.token")

# Schwab API Rate Limit is 120 requests per minute
sch_limiter = AsyncLimiter(max_rate=120, time_period=60)

try:
    sch: AsyncClient = auth.client_from_token_file(
        token_path=SCHWAB_TOKEN_FP,
        api_key=SCHWAB_APP_KEY,
        app_secret=SCHWAB_SECRET,
        asyncio=True,
    )
except FileNotFoundError:
    sch: AsyncClient = auth.client_from_manual_flow(
        api_key=SCHWAB_APP_KEY,
        app_secret=SCHWAB_SECRET,
        callback_url=SCHWAB_REDIRECT_URI,
        token_path=SCHWAB_TOKEN_FP,
        asyncio=True,
    )
