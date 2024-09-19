"""axiom/db/auth.py"""

import json
import os

from axiom.config import DATA_DIR
from axiom.supabase import supabase

TOKEN_BUCKET = "auth"
TOKEN_FP = "schwab.token"


def get_schwab_token_from_db() -> dict | None:
    """Get token from db"""

    # Download the file from the bucket
    with open(DATA_DIR.joinpath(TOKEN_FP), "wb+") as f:
        res = supabase.storage.from_(TOKEN_BUCKET).download(TOKEN_FP)
        if not res:
            return None

        # Write the token to the file
        f.write(res)

    # Set the SCHWAB_TOKEN environment variable
    with open(DATA_DIR.joinpath(TOKEN_FP), "r") as f:
        os.environ["SCHWAB_TOKEN"] = f.read()

    return json.loads(os.getenv("SCHWAB_TOKEN"))


def set_schwab_token_in_db(token: dict) -> None:
    """Set token in db"""

    # Write the token to the file
    with open(DATA_DIR.joinpath(TOKEN_FP), "w", encoding="utf-8") as f:
        json.dump(token, f)

    # Upload the file to the bucket
    with open(DATA_DIR.joinpath(TOKEN_FP), "rb") as f:
        supabase.storage.from_(TOKEN_BUCKET).upload(
            file=f, path=TOKEN_FP, file_options={"cache-control": "0", "upsert": "true"}
        )
