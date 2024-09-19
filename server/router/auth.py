"""server/router/auth.py"""

import json
import os

from authlib.integrations.httpx_client import OAuth2Client
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from schwab.auth import __fetch_and_register_token_from_redirect

from axiom.config import DATA_DIR
from axiom.db.auth import set_schwab_token_in_db

router = APIRouter(prefix="/auth")

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "8123")
if HOST == "localhost":
    REDIRECT_URI = f"https://127.0.0.1:{PORT}/auth/callback"
else:
    REDIRECT_URI = f"https://{HOST}/auth/callback"

SCHWAB_APP_KEY = os.environ["SCHWAB_APP_KEY"]
SCHWAB_SECRET = os.environ["SCHWAB_SECRET"]
SCHWAB_REDIRECT_URI = "https://127.0.0.1"
SCHWAB_TOKEN_FP = DATA_DIR.joinpath("schwab.token")

SCHWAB_OAUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"

oauth = OAuth2Client(SCHWAB_APP_KEY, redirect_uri=REDIRECT_URI)

router = APIRouter(prefix="/auth")


@router.get("/schwab")
async def auth_schwab() -> RedirectResponse:
    authorization_url, state = oauth.create_authorization_url(SCHWAB_OAUTH_URL)
    return RedirectResponse(url=authorization_url)


@router.get("/callback")
async def auth_callback(request: Request) -> JSONResponse:
    redirected_url = str(request.url)

    success = __fetch_and_register_token_from_redirect(
        oauth=oauth,
        redirected_url=redirected_url,
        api_key=SCHWAB_APP_KEY,
        app_secret=SCHWAB_SECRET,
        token_path=SCHWAB_TOKEN_FP,
        token_write_func=None,
        asyncio=False,
        enforce_enums=True,
    )

    if success:
        # Get the token from the file
        with open(SCHWAB_TOKEN_FP, "r", encoding="utf-8") as f:
            token: dict = json.load(f)

        # Set the token in the db
        set_schwab_token_in_db(token)

        return JSONResponse(status_code=200, content={"message": "Authentication successful"})
    else:
        return JSONResponse(status_code=500, content={"message": "Authentication failed"})
