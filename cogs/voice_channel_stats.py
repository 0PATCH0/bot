import discord
from discord.ext import commands
from discord import app_commands

class VoiceChannelStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="voice_stats", description="Показує статистику голосових каналів.")
    async def voice_stats(self, interaction: discord.Interaction):
        """Показує кількість користувачів у голосових каналах."""
        stats = {}
        
        for vc in interaction.guild.voice_channels:
            stats[vc.name] = len(vc.members)
        
        if stats:
            stats_message = "Статистика голосових каналів:\n"
            for channel_name, members in stats.items():
                stats_message += f"{channel_name}: {members} користувачів\n"
            await interaction.response.send_message(stats_message)
        else:
            await interaction.response.send_message("Немає голосових каналів на сервері.")

# Реєстрація розширення
async def setup(bot):
    await bot.add_cog(VoiceChannelStats(bot))
