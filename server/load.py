"""server/load.py"""

from axiom.config import DATA_DIR
from axiom.db.auth import get_schwab_token_from_db
from axiom.models import WeeklyResistanceModel

_weekly_resistance_model: WeeklyResistanceModel | None = None


def download_schwab_token() -> None:
    # Get the token from the database
    # It also sets the local token file
    schwab_token = get_schwab_token_from_db()
    if schwab_token is None:
        raise ValueError("Failed to retrieve Schwab token from database")


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
