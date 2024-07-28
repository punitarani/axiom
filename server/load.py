"""server/load.py"""

import os

from axiom.config import DATA_DIR
from axiom.models import WeeklyResistanceModel
from axiom.schwab_client import SCHWAB_TOKEN_FP

_weekly_resistance_model: WeeklyResistanceModel | None = None


def download_schwab_token() -> None:
    schwab_token = os.getenv("SCHWAB_TOKEN", None)
    if schwab_token is not None:
        with open(SCHWAB_TOKEN_FP, "w") as f:
            f.write(schwab_token)

    raise ValueError("SCHWAB_TOKEN environment variable not set")


async def load_models():
    await load_weekly_resistance_model()


async def load_weekly_resistance_model():
    weekly_resistance_model_high_fp = DATA_DIR.joinpath(
        "models", "weekly_resistance_model_high_SPY.json"
    )
    weekly_resistance_model_low_fp = DATA_DIR.joinpath(
        "models", "weekly_resistance_model_low_SPY.json"
    )

    # Load the pipeline
    pipeline = WeeklyResistanceModel.load(
        "SPY", weekly_resistance_model_high_fp, weekly_resistance_model_low_fp
    )

    # Store the pipeline
    global _weekly_resistance_model
    _weekly_resistance_model = pipeline


async def get_weekly_resistance_model() -> WeeklyResistanceModel:
    return _weekly_resistance_model
