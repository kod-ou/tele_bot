import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SUPABASE_URL = os.getenv('VITE_SUPABASE_URL')
SUPABASE_KEY = os.getenv('VITE_SUPABASE_ANON_KEY')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
if not SUPABASE_URL:
    raise ValueError("VITE_SUPABASE_URL not found in environment variables")
if not SUPABASE_KEY:
    raise ValueError("VITE_SUPABASE_ANON_KEY not found in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
