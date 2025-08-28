from supabase import Client, create_client

from axiom.env import env

# Create Supabase client using validated environment variables
supabase: Client = create_client(str(env.SUPABASE_URL), env.SUPABASE_SERVICE_KEY)
