import discord
from discord.ext import commands, tasks
from discord import app_commands
import logging
from datetime import datetime, timedelta
import asyncio

logger = logging.getLogger(__name__)

class EventScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events = {}

    @app_commands.command(name="add_event", description="Додає подію з нагадуванням.")
    async def add_event(self, interaction: discord.Interaction, time: str, *, description: str, channel: discord.TextChannel):
        """Додає подію. Формат часу: 'YYYY-MM-DD HH:MM'."""
        try:
            event_time = datetime.strptime(time, '%Y-%m-%d %H:%M')
            if event_time < datetime.now():
                await interaction.response.send_message("❌ Подія не може бути в минулому!")
                return
            self.events[event_time] = {
                "description": description,
                "channel_id": channel.id
            }
            await interaction.response.send_message(f"✅ Подія `{description}` додана на {event_time}. Я нагадаю вам про це!")

            # Стартуємо задачу для нагадування
            await self.send_reminder(event_time, description, channel)

        except ValueError:
            await interaction.response.send_message("❌ Невірний формат часу! Використовуйте 'YYYY-MM-DD HH:MM'.")

    async def send_reminder(self, event_time, description, channel):
        """Відправляє нагадування про подію в чат."""
        await asyncio.sleep((event_time - datetime.now()).total_seconds())  # Чекає до події
        try:
            channel = self.bot.get_channel(channel.id)
            if channel:
                await channel.send(f"🔔 Нагадування! Подія: {description} відбудеться зараз! 🎉")
            else:
                logger.error("Канал для нагадування не знайдений.")
        except Exception as e:
            logger.error(f"Помилка при надсиланні нагадування: {e}")

async def setup(bot):
    await bot.add_cog(EventScheduler(bot))
