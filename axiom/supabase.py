"""axiom/supabase.py"""

import os

from supabase import Client, create_client

_SUPABASE_URL: str = os.environ["SUPABASE_URL"]
_SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(_SUPABASE_URL, _SUPABASE_KEY)
