"""axiom/config.py"""

import os
from pathlib import Path
from typing import List

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR.joinpath("data")


def ensure_env_vars():
    """Ensure all environment variables are set."""
    required_vars: List[str] = [
        "MODE",
        "HOST",
        "PORT",
        "SCHWAB_APP_KEY",
        "SCHWAB_SECRET",
        "SUPABASE_URL",
        "SUPABASE_KEY",
    ]

    missing_vars = [var for var in required_vars if var not in os.environ]

    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
