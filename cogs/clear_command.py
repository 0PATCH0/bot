import discord
from discord import app_commands
from discord.ext import commands

class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Очищає певну кількість повідомлень.")
    @app_commands.describe(amount="Кількість повідомлень для видалення")
    async def clear(self, interaction: discord.Interaction, amount: int):
        """Очищає задану кількість повідомлень."""
        if amount <= 0:
            await interaction.response.send_message("❌ Кількість повідомлень має бути більшою за 0!", ephemeral=True)
            return
        
        # Очищення повідомлень
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"✅ Видалено {len(deleted)} повідомлень!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ClearCommand(bot))  # Додав команду очищення
