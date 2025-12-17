import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SUPABASE_URL = os.getenv('VITE_SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('VITE_SUPABASE_SERVICE_ROLE_KEY')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
if not SUPABASE_URL:
    raise ValueError("VITE_SUPABASE_URL not found in environment variables")
if not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError(
        "VITE_SUPABASE_SERVICE_ROLE_KEY not found in environment variables.\n"
        "Please get your service role key from: https://supabase.com/dashboard/project/zetgffumucclwevnkfww/settings/api"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
