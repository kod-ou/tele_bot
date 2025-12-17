import random
from telegram import Update
from telegram.ext import ContextTypes
from config import supabase

async def send_random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random motivational quote"""
    chat_id = update.effective_chat.id

    try:
        settings_result = supabase.table('group_settings').select('quotes_enabled').eq('chat_id', chat_id).execute()

        if settings_result.data and len(settings_result.data) > 0:
            quotes_enabled = settings_result.data[0].get('quotes_enabled', True)
            if not quotes_enabled:
                await update.message.reply_text("Quote feature tidak aktif untuk group ini.")
                return

        quotes_result = supabase.table('motivational_quotes').select('*').eq('is_active', True).execute()

        if not quotes_result.data:
            await update.message.reply_text("Tiada quote tersedia pada masa ini.")
            return

        quote = random.choice(quotes_result.data)
        quote_text = quote.get('quote_text')
        author = quote.get('author', '')

        message = f"💡 *Quote Motivasi*\n\n_{quote_text}_"
        if author:
            message += f"\n\n— {author}"

        await update.message.reply_text(message, parse_mode='Markdown')

    except Exception as e:
        print(f"Error sending quote: {e}")
        await update.message.reply_text("Maaf, terjadi kesalahan saat mengambil quote.")

async def send_quote_to_chat(bot, chat_id):
    """Send a random quote to a specific chat (for scheduler)"""
    try:
        settings_result = supabase.table('group_settings').select('quotes_enabled').eq('chat_id', chat_id).execute()

        if settings_result.data and len(settings_result.data) > 0:
            quotes_enabled = settings_result.data[0].get('quotes_enabled', True)
            if not quotes_enabled:
                return

        quotes_result = supabase.table('motivational_quotes').select('*').eq('is_active', True).execute()

        if not quotes_result.data:
            return

        quote = random.choice(quotes_result.data)
        quote_text = quote.get('quote_text')
        author = quote.get('author', '')

        message = f"💡 *Quote Motivasi*\n\n_{quote_text}_"
        if author:
            message += f"\n\n— {author}"

        await bot.send_message(chat_id, message, parse_mode='Markdown')

    except Exception as e:
        print(f"Error sending scheduled quote: {e}")
