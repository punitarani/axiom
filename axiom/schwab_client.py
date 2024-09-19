"""axiom/schwab_client.py"""

import os

from aiolimiter import AsyncLimiter
from schwab import auth
from schwab.client import AsyncClient

from axiom.config import DATA_DIR

SCHWAB_APP_KEY = os.environ["SCHWAB_APP_KEY"]
SCHWAB_SECRET = os.environ["SCHWAB_SECRET"]
SCHWAB_REDIRECT_URI = "https://127.0.0.1:8123"
SCHWAB_TOKEN_FP = DATA_DIR.joinpath("schwab.token")

# Schwab API Rate Limit is 120 requests per minute
sch_limiter = AsyncLimiter(max_rate=120, time_period=60)


def get_schwab_client() -> AsyncClient:
    return auth.client_from_token_file(
        token_path=SCHWAB_TOKEN_FP,
        api_key=SCHWAB_APP_KEY,
        app_secret=SCHWAB_SECRET,
        asyncio=True,
    )
