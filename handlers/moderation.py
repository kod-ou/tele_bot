import re
from telegram import Update
from telegram.ext import ContextTypes
from config import supabase
from datetime import datetime

URL_PATTERN = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)

async def check_message_for_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check messages for unauthorized links and issue warnings"""
    if not update.message or not update.message.text:
        return

    message = update.message
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    try:
        settings_result = supabase.table('group_settings').select('link_moderation_enabled, max_warnings').eq('chat_id', chat_id).execute()

        if not settings_result.data or len(settings_result.data) == 0:
            return

        link_moderation_enabled = settings_result.data[0].get('link_moderation_enabled', True)
        max_warnings = settings_result.data[0].get('max_warnings', 3)

        if not link_moderation_enabled:
            return

        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        if user_id in admin_ids:
            return

        if URL_PATTERN.search(message.text):
            await message.delete()

            warning_result = supabase.table('user_warnings').select('*').eq('user_id', user_id).eq('chat_id', chat_id).execute()

            if warning_result.data and len(warning_result.data) > 0:
                new_count = warning_result.data[0]['warning_count'] + 1

                supabase.table('user_warnings').update({
                    'warning_count': new_count,
                    'last_warning_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }).eq('user_id', user_id).eq('chat_id', chat_id).execute()

                if new_count >= max_warnings:
                    try:
                        await context.bot.ban_chat_member(chat_id, user_id)

                        supabase.table('user_warnings').delete().eq('user_id', user_id).eq('chat_id', chat_id).execute()

                        warning_msg = f"⛔️ {username} telah dikeluarkan dari group kerana mencapai {max_warnings} amaran!"
                        await context.bot.send_message(chat_id, warning_msg)
                    except Exception as e:
                        print(f"Error kicking user: {e}")
                        await context.bot.send_message(chat_id, f"⚠️ Tidak dapat mengeluarkan {username}. Bot mungkin tidak mempunyai kebenaran admin.")
                else:
                    warning_msg = f"⚠️ {username}, link tidak dibenarkan! Amaran {new_count}/{max_warnings}"
                    await context.bot.send_message(chat_id, warning_msg)
            else:
                supabase.table('user_warnings').insert({
                    'user_id': user_id,
                    'chat_id': chat_id,
                    'username': username,
                    'warning_count': 1
                }).execute()

                warning_msg = f"⚠️ {username}, link tidak dibenarkan! Amaran 1/{max_warnings}"
                await context.bot.send_message(chat_id, warning_msg)

    except Exception as e:
        print(f"Error in moderation handler: {e}")
