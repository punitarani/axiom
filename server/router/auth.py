"""server/router/auth.py"""

import os

from authlib.oauth2 import OAuth2Client
from config import DATA_DIR
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response
from schwab.auth import __fetch_and_register_token_from_redirect

router = APIRouter(prefix="/auth")

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "8123")
if HOST == "localhost":
    REDIRECT_URI = f"http://{HOST}:{PORT}/auth/callback"
else:
    REDIRECT_URI = f"https://{HOST}/auth/callback"

SCHWAB_APP_KEY = os.environ["SCHWAB_APP_KEY"]
SCHWAB_SECRET = os.environ["SCHWAB_SECRET"]
SCHWAB_REDIRECT_URI = "https://127.0.0.1"
SCHWAB_TOKEN_FP = DATA_DIR.joinpath("schwab.token")

SCHWAB_OAUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"

oauth = OAuth2Client(SCHWAB_APP_KEY, redirect_uri=REDIRECT_URI)

auth_router = APIRouter()


@auth_router.get("/auth/schwab")
async def auth_schwab() -> RedirectResponse:
    authorization_url, state = oauth.create_authorization_url(SCHWAB_OAUTH_URL)
    return RedirectResponse(url=authorization_url)


@auth_router.get("/auth/callback")
async def auth_callback(request: Request) -> Response:
    redirected_url = request.url

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
        return Response(status_code=200)
    else:
        return Response(status_code=500)
