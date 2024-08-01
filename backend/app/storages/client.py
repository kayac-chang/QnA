from supabase import Client, create_client

from app.config import settings

url: str = settings.SUPABASE_API_URL
key: str = settings.SUPABASE_API_KEY
supabase: Client = create_client(url, key)
