"""axiom package"""

from dotenv import load_dotenv

from .config import PROJECT_DIR

ENV_FP = PROJECT_DIR.joinpath(".env")
load_dotenv(ENV_FP)
