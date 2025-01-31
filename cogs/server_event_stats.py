import discord
from discord.ext import commands
from discord import app_commands

class ServerEventStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="server_stats", description="Показує статистику подій на сервері.")
    async def server_stats(self, interaction: discord.Interaction):
        """Показує дату створення сервера та кількість активних користувачів."""
        server = interaction.guild
        creation_date = server.created_at.strftime("%Y-%m-%d %H:%M:%S")
        active_members = sum(1 for member in server.members if member.status != discord.Status.offline)

        stats_message = (
            f"Статистика сервера:\n"
            f"📅 Дата створення: {creation_date}\n"
            f"👥 Кількість активних користувачів: {active_members}/{len(server.members)}"
        )

        await interaction.response.send_message(stats_message)

# Реєстрація розширення
async def setup(bot):
    await bot.add_cog(ServerEventStats(bot))
