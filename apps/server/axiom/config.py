import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

# Schwab OAuth configuration
SCHWAB_API_KEY = os.getenv("SCHWAB_API_KEY")
SCHWAB_APP_SECRET = os.getenv("SCHWAB_APP_SECRET")
SCHWAB_CALLBACK_URL = os.getenv(
    "SCHWAB_CALLBACK_URL", "https://127.0.0.1:8000/api/schwab/callback"
)

# Owner ID for access control
OWNER_ID = os.getenv("OWNER_ID")

if not all([SUPABASE_URL, SUPABASE_SERVICE_KEY]):
    raise ValueError("Missing required Supabase configuration")

if not all([SCHWAB_API_KEY, SCHWAB_APP_SECRET, OWNER_ID]):
    raise ValueError("Missing required Schwab OAuth or OWNER_ID configuration")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
