import discord
from discord.ext import commands
from discord import app_commands
import logging
from config import load_config, save_config
from typing import Optional

logger = logging.getLogger(__name__)

class VoiceRoles(commands.Cog):
    """
    Cog для автоматичного призначення ролей користувачам, які входять у голосові канали.
    """

    def __init__(self, bot: commands.Bot):
        """
        Ініціалізує Cog.

        Args:
            bot (commands.Bot): Екземпляр бота.
        """
        self.bot = bot
        self.config = load_config()

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Автоматичне призначення ролей користувачам, які вже знаходяться в голосових каналах після перезавантаження бота.
        """
        guild = self.bot.guilds[0]  # Припускаємо, що бот тільки на одному сервері
        voice_roles = self.config.get("voice_roles", {})

        for channel in guild.voice_channels:
            category_id = str(channel.category.id)
            role_id = voice_roles.get(category_id)

            if role_id:
                role = guild.get_role(int(role_id))
                if role:
                    for member in channel.members:
                        if role not in member.roles:
                            try:
                                await member.add_roles(role, reason="Приєднання до голосового каналу після перезавантаження бота")
                                logger.info(f"Роль {role.name} надано користувачу {member.name} в каналі {channel.name}.")
                            except Exception as e:
                                logger.error(f"Не вдалося додати роль: {e}")
                else:
                    logger.error(f"Роль з ID {role_id} не знайдена для категорії {category_id}.")
            else:
                logger.warning(f"Не знайдена роль для категорії {category_id}.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """
        Видає або забирає роль при вході/виході з голосового каналу.

        Args:
            member (discord.Member): Користувач, який змінив стан голосового каналу.
            before (discord.VoiceState): Попередній стан голосового каналу.
            after (discord.VoiceState): Новий стан голосового каналу.
        """
        guild = member.guild
        voice_roles = self.config.get("voice_roles", {})

        # Якщо користувач приєднався до голосового каналу
        if after.channel and after.channel != before.channel:
            await self._handle_voice_role(member, after.channel, "Приєднався до голосового каналу")

        # Якщо користувач покинув голосовий канал
        if before.channel and before.channel != after.channel:
            await self._handle_voice_role(member, before.channel, "Покинув голосовий канал", remove=True)

    async def _handle_voice_role(self, member: discord.Member, channel: discord.VoiceChannel, reason: str, remove: bool = False):
        """
        Обробляє призначення або видалення ролі для голосового каналу.

        Args:
            member (discord.Member): Користувач, який змінив стан голосового каналу.
            channel (discord.VoiceChannel): Голосовий канал.
            reason (str): Причина зміни ролі.
            remove (bool): Чи потрібно видалити роль (за замовчуванням False).
        """
        category_id = str(channel.category.id)
        role_id = self.config.get("voice_roles", {}).get(category_id)

        if role_id:
            role = member.guild.get_role(int(role_id))
            if role:
                try:
                    if remove:
                        if role in member.roles:
                            await member.remove_roles(role, reason=reason)
                            logger.info(f"Роль {role.name} успішно видалено у {member.name}.")
                    else:
                        if role not in member.roles:
                            await member.add_roles(role, reason=reason)
                            logger.info(f"Роль {role.name} надано користувачу {member.name}.")
                except Exception as e:
                    logger.error(f"Не вдалося змінити роль: {e}")
            else:
                logger.error(f"Роль з ID {role_id} не знайдена.")
        else:
            logger.warning(f"Не налаштовано роль для категорії {category_id}.")

    @app_commands.command(name="set_voice_role", description="Налаштувати роль для голосового каналу")
    @app_commands.describe(category_id="ID категорії голосового каналу", role_id="ID ролі")
    async def set_voice_role(self, interaction: discord.Interaction, category_id: str, role_id: str):
        """
        Налаштовує роль для голосового каналу.

        Args:
            interaction (discord.Interaction): Взаємодія з користувачем.
            category_id (str): ID категорії голосового каналу.
            role_id (str): ID ролі.
        """
        try:
            category_id = int(category_id)
            role_id = int(role_id)

            if "voice_roles" not in self.config:
                self.config["voice_roles"] = {}

            self.config["voice_roles"][str(category_id)] = str(role_id)
            save_config(self.config)

            await interaction.response.send_message(
                f"✅ Роль <@&{role_id}> успішно налаштована для категорії <#{category_id}>.",
                ephemeral=True
            )
            logger.info(f"Категорія {category_id} пов'язана з роллю {role_id}.")
        except ValueError:
            await interaction.response.send_message("❌ Введіть дійсне число для ID.", ephemeral=True)
            logger.error("Невірний формат ID.")
        except Exception as e:
            await interaction.response.send_message("❌ Сталася помилка при налаштуванні ролі.", ephemeral=True)
            logger.error(f"Помилка: {e}")

async def setup(bot: commands.Bot):
    """
    Завантажує Cog та реєструє його в боті.

    Args:
        bot (commands.Bot): Екземпляр бота.
    """
    await bot.add_cog(VoiceRoles(bot))