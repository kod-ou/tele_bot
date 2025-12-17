from telegram import Update
from telegram.ext import ContextTypes
from config import supabase

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message to new group members"""
    if not update.message or not update.message.new_chat_members:
        return

    chat_id = update.effective_chat.id

    try:
        result = supabase.table('group_settings').select('welcome_message').eq('chat_id', chat_id).execute()

        if result.data and len(result.data) > 0:
            welcome_message = result.data[0].get('welcome_message', 'Group ini akan bagi tips harian mana game yang muntah 🤑, lebih beratus ahli dalam group ini biasa kasi out hari-hari...')
        else:
            welcome_message = 'Group ini akan bagi tips harian mana game yang muntah 🤑, lebih beratus ahli dalam group ini biasa kasi out hari-hari...'
            supabase.table('group_settings').insert({
                'chat_id': chat_id,
                'chat_title': update.effective_chat.title or '',
                'welcome_message': welcome_message
            }).execute()

        for new_member in update.message.new_chat_members:
            if not new_member.is_bot:
                greeting = f"Selamat datang kepada {new_member.first_name} 🥳\n\n{welcome_message}"
                await update.message.reply_text(greeting)

    except Exception as e:
        print(f"Error in welcome handler: {e}")
        await update.message.reply_text("Selamat datang ke group! 🥳")
