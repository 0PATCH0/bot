import discord
from discord.ext import commands
from discord import app_commands
import logging
import requests
from config import load_config, save_config
from typing import Dict, Any, Optional

# Налаштовуємо логування
logging.basicConfig(
    level=logging.INFO,  # Визначаємо мінімальний рівень логування
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),  # Записуємо логи в файл
        logging.StreamHandler()  # Виводимо логи в консоль
    ]
)
logger = logging.getLogger(__name__)

class TelegramWebhook(commands.Cog):
    """
    Cog для інтеграції Telegram з Discord через вебхуки.
    """

    def __init__(self, bot: commands.Bot):
        """
        Ініціалізує Cog.

        Args:
            bot (commands.Bot): Екземпляр бота.
        """
        self.bot = bot
        self.config = load_config()
        logger.info("TelegramWebhook Cog ініціалізовано.")

    @app_commands.command(name="set_telegram_webhook", description="Налаштувати Telegram-канал, токен і вебхук Discord")
    @app_commands.describe(
        telegram_channel_id="ID Telegram-каналу",
        telegram_token="Токен Telegram-бота",
        discord_webhook_url="URL вебхука Discord"
    )
    async def set_telegram_webhook(self, interaction: discord.Interaction, telegram_channel_id: str, telegram_token: str, discord_webhook_url: str):
        """
        Налаштовує Telegram-канал, токен бота та вебхук Discord для пересилання повідомлень.

        Args:
            interaction (discord.Interaction): Взаємодія з користувачем.
            telegram_channel_id (str): ID Telegram-каналу.
            telegram_token (str): Токен Telegram-бота.
            discord_webhook_url (str): URL вебхука Discord.
        """
        try:
            if not telegram_channel_id or not telegram_token or not discord_webhook_url:
                await interaction.response.send_message("❌ Будь ласка, введіть усі необхідні параметри.", ephemeral=True)
                logger.warning("Не всі параметри надано для налаштування.")
                return

            # Збереження налаштувань у конфігурації
            self.config["telegram_webhook"] = {
                "telegram_channel_id": telegram_channel_id,
                "telegram_token": telegram_token,
                "discord_webhook_url": discord_webhook_url,
            }
            save_config(self.config)

            await interaction.response.send_message(
                f"✅ Налаштування збережено!\n"
                f"📢 Telegram-канал: `{telegram_channel_id}`\n"
                f"🔑 Токен: `{telegram_token}`\n"
                f"🌍 Вебхук Discord: `{discord_webhook_url}`",
                ephemeral=True,
            )
            logger.info(f"Налаштування збережено: Telegram-канал {telegram_channel_id}, вебхук Discord: {discord_webhook_url}")
        except Exception as e:
            await interaction.response.send_message("❌ Сталася помилка при налаштуванні.", ephemeral=True)
            logger.error(f"Помилка при налаштуванні Telegram webhook: {e}")

    async def send_message_to_discord(self, message: str, webhook_url: str) -> bool:
        """
        Відправляє текстове повідомлення в Discord через вебхук.

        Args:
            message (str): Текстове повідомлення.
            webhook_url (str): URL вебхука Discord.

        Returns:
            bool: Чи вдалося відправити повідомлення.
        """
        try:
            data = {"content": message}
            response = requests.post(webhook_url, json=data)
            if response.status_code == 204:
                logger.info(f"Повідомлення успішно надіслано в Discord: {message}")
                return True
            else:
                logger.error(f"Помилка при відправленні повідомлення в Discord: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Помилка при відправленні повідомлення: {e}")
            return False

    async def handle_telegram_message(self, update: Dict[str, Any]) -> None:
        """
        Обробляє повідомлення з Telegram та пересилає його в Discord.

        Args:
            update (Dict[str, Any]): Оновлення з Telegram (повідомлення).
        """
        try:
            telegram_message = update.get("message", {}).get("text", "")
            if not telegram_message:
                logger.warning("Повідомлення з Telegram не містить тексту.")
                return

            discord_webhook_url = self.config.get("telegram_webhook", {}).get("discord_webhook_url")
            if not discord_webhook_url:
                logger.error("Вебхук Discord не налаштовано.")
                return

            # Відправляємо повідомлення в Discord
            await self.send_message_to_discord(telegram_message, discord_webhook_url)
        except Exception as e:
            logger.error(f"Помилка при обробці повідомлення з Telegram: {e}")

async def setup(bot: commands.Bot):
    """
    Завантажує Cog та реєструє його в боті.

    Args:
        bot (commands.Bot): Екземпляр бота.
    """
    await bot.add_cog(TelegramWebhook(bot))
    try:
        await bot.tree.sync()  # Синхронізує команди з Discord
        logger.info("Синхронізація команд завершена успішно.")
    except Exception as e:
        logger.error(f"Помилка при синхронізації команд: {e}")
