import asyncio
from datetime import datetime
from config import supabase

class MessageScheduler:
    def __init__(self, bot):
        self.bot = bot
        self.running = False

    async def start(self):
        """Start the scheduler loop"""
        self.running = True
        while self.running:
            await self.check_and_send_scheduled_messages()
            await asyncio.sleep(60)

    async def check_and_send_scheduled_messages(self):
        """Check for scheduled messages and send them"""
        try:
            current_time = datetime.now()
            current_day = current_time.strftime('%A').lower()
            current_hour_minute = current_time.strftime('%H:%M')

            result = supabase.table('scheduled_messages').select('*').eq('is_active', True).execute()

            for message in result.data:
                schedule_time = message.get('schedule_time')
                schedule_days = message.get('schedule_days', [])

                if schedule_time == current_hour_minute:
                    if not schedule_days or current_day in [day.lower() for day in schedule_days]:
                        chat_id = message.get('chat_id')
                        message_text = message.get('message_text')

                        try:
                            await self.bot.send_message(chat_id, message_text)
                            print(f"Sent scheduled message to {chat_id}")
                        except Exception as e:
                            print(f"Error sending scheduled message: {e}")

        except Exception as e:
            print(f"Error in scheduler: {e}")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
