import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from handlers.welcome import welcome_new_member
from handlers.moderation import check_message_for_links
from handlers.quotes import send_random_quote
from services.scheduler import MessageScheduler

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🤖 Selamat datang! Saya adalah bot pengurus group.\n\n"
        "Saya boleh membantu dengan:\n"
        "✅ Menghantar mesej welcome kepada ahli baru\n"
        "✅ Moderasi link dalam group\n"
        "✅ Sistem amaran automatik\n"
        "✅ Hantar mesej berjadual\n"
        "✅ Kongsi quote motivasi\n\n"
        "Gunakan /help untuk melihat semua command."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "📚 *Command Bot*\n\n"
        "/start - Mulakan bot\n"
        "/help - Paparkan bantuan\n"
        "/quote - Dapatkan quote motivasi rawak\n"
        "/stats - Lihat statistik amaran\n\n"
        "*Features Aktif:*\n"
        "🔹 Welcome message untuk ahli baru\n"
        "🔹 Auto-delete link tidak dibenarkan\n"
        "🔹 Sistem amaran 3 kali sebelum kick\n"
        "🔹 Mesej berjadual\n"
        "🔹 Quote motivasi harian"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show warning statistics for the user"""
    from config import supabase

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    try:
        result = supabase.table('user_warnings').select('*').eq('user_id', user_id).eq('chat_id', chat_id).maybeSingle().execute()

        if result.data:
            warning_count = result.data.get('warning_count', 0)
            await update.message.reply_text(
                f"⚠️ *Statistik Amaran Anda*\n\n"
                f"Amaran: {warning_count}/3\n"
                f"Status: {'Bahaya! Satu lagi amaran akan menyebabkan anda dikeluarkan!' if warning_count >= 2 else 'Sila patuhi peraturan group.'}"
                , parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("✅ Anda tidak mempunyai amaran. Teruskan!")

    except Exception as e:
        print(f"Error fetching stats: {e}")
        await update.message.reply_text("Maaf, terjadi kesalahan saat mengambil statistik.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    print("🚀 Starting Telegram Bot...")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("quote", send_random_quote))
    application.add_handler(CommandHandler("stats", stats_command))

    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message_for_links))

    application.add_error_handler(error_handler)

    scheduler = MessageScheduler(application.bot)

    async def post_init(app: Application):
        """Run after bot initialization"""
        asyncio.create_task(scheduler.start())
        print("✅ Bot is running and scheduler started!")

    application.post_init = post_init

    print("✅ Bot initialized successfully!")
    print("📡 Polling for updates...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
