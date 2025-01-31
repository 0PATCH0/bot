import sys
import asyncio
import discord
from discord.ext import commands
import logging
from config import TOKEN
from cogs.voice_roles import VoiceRoles
from cogs.telegram_webhook import TelegramWebhook
from cogs.voice_channel_stats import VoiceChannelStats  # Додав команду статистики голосових каналів
from cogs.server_event_stats import ServerEventStats  # Додав команду статистики сервера
from cogs.help_command import HelpCommand  # Додав команду допомоги
from cogs.event_scheduler import EventScheduler  # Додав EventScheduler
from cogs.clear_command import ClearCommand  # Додав команду очищення


# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),  # Лог у файл
        logging.StreamHandler(sys.stdout)  # Вивід у консоль
    ]
)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True  # Важливо для слеш-команд

bot = commands.Bot(command_prefix="!", intents=intents)

# Функція зміни статусу
async def change_status():
    """Змінює статус бота кожні 5 хвилин."""
    STATUS_LIST = [
        "Reaper фармить ліс",
        "Аскет без інтернет кабеля",
        "Matsui Спостерігає",
        "Joe Posranchik знову фідить",
        "PATCH БОЖЕСТВО"
    ]
    while True:
        for status in STATUS_LIST:
            await bot.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(300)  # Чекаємо 5 хвилин

@bot.event
async def on_ready():
    """Коли бот готовий до роботи."""
    logger.info(f'Бот {bot.user} готовий до роботи!')
    try:
        # Синхронізуємо всі команди з усіх Cogs
        synced = await bot.tree.sync()
        logger.info(f"Синхронізовано {len(synced)} команд.")
    except Exception as e:
        logger.error(f"Помилка синхронізації команд: {e}")


    # Запускаємо завдання для зміни статусу
    bot.loop.create_task(change_status())

# Завантаження розширень
async def setup_extensions():
    """Завантажує всі розширення (Cogs)."""
    try:
        await bot.add_cog(VoiceRoles(bot))
        await bot.add_cog(TelegramWebhook(bot))
        await bot.add_cog(VoiceChannelStats(bot))  # Додав команду статистики голосових каналів
        await bot.add_cog(ServerEventStats(bot))   # Додав команду статистики сервера
        await bot.add_cog(HelpCommand(bot))         # Додав команду допомоги
        await bot.add_cog(EventScheduler(bot))      # Додав EventScheduler
        await bot.add_cog(ClearCommand(bot))        # Додав команду очищення
        logger.info("Усі Cogs успішно завантажено!")
    except Exception as e:
        logger.error(f"Помилка при завантаженні Cogs: {e}")


# Основна частина для запуску бота
async def main():
    """Запускає бота."""
    async with bot:
        await setup_extensions()  # Завантажує всі розширення
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
