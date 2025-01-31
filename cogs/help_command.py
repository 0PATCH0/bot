import discord
from discord.ext import commands
from discord import app_commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Показує список всіх доступних команд.")
    async def help_command(self, interaction: discord.Interaction):
        """Виводить список команд та їх опис."""
        help_text = """
        **Доступні команди:**

        /add_event <time> <description> - Додає подію з нагадуванням. Формат часу: 'YYYY-MM-DD HH:MM'.
        /voice_stats - Показує статистику по голосових каналах.
        /server_stats - Показує статистику сервера.
        /set_telegram_webhook - Налаштування Telegram-каналу, токена і вебхука Discord.
        """
        await interaction.response.send_message(help_text, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
    await bot.tree.sync()  # Додано для синхронізації команд
