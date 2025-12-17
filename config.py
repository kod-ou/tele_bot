import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('8119606757:AAEqkm1FyBu51bmeb4sS5PLj0dSoFZAv_nI')
SUPABASE_URL = os.getenv('https://zetgffumucclwevnkfww.supabase.co')
SUPABASE_KEY = os.getenv('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpldGdmZnVtdWNjbHdldm5rZnd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5MzA5NzMsImV4cCI6MjA4MTUwNjk3M30.4C7qp_90KBnIstmzMYXY08BoNXj9-qMR-7cY6DJDvhk')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("8119606757:AAEqkm1FyBu51bmeb4sS5PLj0dSoFZAv_nI")
if not SUPABASE_URL:
    raise ValueError("https://zetgffumucclwevnkfww.supabase.co")
if not SUPABASE_KEY:
    raise ValueError("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpldGdmZnVtdWNjbHdldm5rZnd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5MzA5NzMsImV4cCI6MjA4MTUwNjk3M30.4C7qp_90KBnIstmzMYXY08BoNXj9-qMR-7cY6DJDvhk")

supabase: Client = create_client(https://zetgffumucclwevnkfww.supabase.co, eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpldGdmZnVtdWNjbHdldm5rZnd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5MzA5NzMsImV4cCI6MjA4MTUwNjk3M30.4C7qp_90KBnIstmzMYXY08BoNXj9-qMR-7cY6DJDvhk)
