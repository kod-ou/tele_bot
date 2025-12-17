import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SUPABASE_URL = os.getenv('VITE_SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('VITE_SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_ANON_KEY = os.getenv('VITE_SUPABASE_ANON_KEY')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
if not SUPABASE_URL:
    raise ValueError("VITE_SUPABASE_URL not found in environment variables")

# Use service role key if available, fallback to anon key
if SUPABASE_SERVICE_ROLE_KEY and SUPABASE_SERVICE_ROLE_KEY != 'YOUR_SERVICE_ROLE_KEY_HERE':
    supabase_key = SUPABASE_SERVICE_ROLE_KEY
    print("Using Supabase service role key")
elif SUPABASE_ANON_KEY:
    supabase_key = SUPABASE_ANON_KEY
    print("Using Supabase anon key (service role key not configured)")
else:
    raise ValueError("No valid Supabase key found in environment variables")

supabase: Client = create_client(SUPABASE_URL, supabase_key)
