import discord
from discord import app_commands, Interaction, Embed
from discord.ext import commands
from discord.ext.commands import CooldownMapping, BucketType

# ------------------------------
# SETTINGS
# ------------------------------
ASSISTANCE_ROLE_ID = 1416873422234845284   # Officers who can request assistance
FORCE_REQUEST_ROLE_ID = 1416873405411491940  # Supervisors who can force request
ADMIN_USER_ID = 1221986685634613338        # Developer override
ASSISTANCE_CHANNEL_ID = 1418416970147299400  # Assistance request channel

DEPARTMENT_LOGO = "https://cdn.discordapp.com/attachments/1231290151708131379/1403809096544813109/Untitled_design__3_-removebg-preview.png?ex=68c9ae1a&is=68c85c9a&hm=a885942430a9f12904a8aa0695e9bdad5af427377c3f7d5c0d9f3788b994678b&"
COLOR_SCHEME = 0x8A8A8A  # Department gray

ASSISTANCE_COOLDOWN = CooldownMapping.from_cooldown(1, 21600, BucketType.user)  # 6 hours


def can_use_assistance_command(user):
    return any(role.id == ASSISTANCE_ROLE_ID for role in user.roles) or user.id == ADMIN_USER_ID


def can_use_force_request(user):
    return any(role.id == FORCE_REQUEST_ROLE_ID for role in user.roles) or user.id == ADMIN_USER_ID


class AssistanceCog(commands.Cog):
    """Handles officer assistance requests."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="assistance-request", description="Send an assistance request with priority and reason")
    @app_commands.describe(
        priority="Priority level of assistance",
        reason="Reason for the assistance request"
    )
    @app_commands.choices(priority=[
        app_commands.Choice(name="1 - Urgent (Ping @everyone)", value=1),
        app_commands.Choice(name="2 - High (Ping @here)", value=2),
        app_commands.Choice(name="3 - Normal (No ping)", value=3)
    ])
    async def assistance_request(self, interaction: Interaction, priority: app_commands.Choice[int], reason: str):
        if not can_use_assistance_command(interaction.user):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        bucket = ASSISTANCE_COOLDOWN.get_bucket(interaction)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            hours = int(retry_after // 3600)
            minutes = int((retry_after % 3600) // 60)
            await interaction.response.send_message(
                f"You must wait {hours}h {minutes}m before using this command again.",
                ephemeral=True
            )
            return

        await self._send_assistance_embed(interaction, priority.value, reason)
        await interaction.response.send_message(
            f"Assistance request sent with priority {priority.value}.", ephemeral=True
        )

    @app_commands.command(name="force-request", description="Force send an assistance request without cooldown")
    @app_commands.describe(
        priority="Priority level of assistance",
        reason="Reason for the assistance request"
    )
    @app_commands.choices(priority=[
        app_commands.Choice(name="1 - Urgent (Ping @everyone)", value=1),
        app_commands.Choice(name="2 - High (Ping @here)", value=2),
        app_commands.Choice(name="3 - Normal (No ping)", value=3)
    ])
    async def force_request(self, interaction: Interaction, priority: app_commands.Choice[int], reason: str):
        if not can_use_force_request(interaction.user):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await self._send_assistance_embed(interaction, priority.value, reason)
        await interaction.response.send_message(
            f"Force assistance request sent with priority {priority.value}.", ephemeral=True
        )

    async def _send_assistance_embed(self, interaction: Interaction, priority_value: int, reason: str):
        channel = interaction.guild.get_channel(ASSISTANCE_CHANNEL_ID)
        if channel is None:
            await interaction.response.send_message("Assistance channel not found.", ephemeral=True)
            return

        if priority_value == 1:
            ping = "@everyone"
            desc_text = "is urgently requesting additional officers."
        elif priority_value == 2:
            ping = "@here"
            desc_text = "is requesting additional officers."
        else:
            ping = None
            desc_text = "is requesting officer assistance."

        description = f"The department {desc_text}\n\n**Reason:** {reason}"
        embed = Embed(
            title="Assistance Request",
            description=description,
            color=COLOR_SCHEME
        )
        embed.set_thumbnail(url=DEPARTMENT_LOGO)

        await channel.send(content=ping, embed=embed)


# ------------------------------
# SETUP
# ------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(AssistanceCog(bot))
