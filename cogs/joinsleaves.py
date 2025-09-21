import discord
from discord.ext import commands
from datetime import datetime, timezone

# ------------------------------
# SETTINGS
# ------------------------------
GUILD_ID = 1416869400748757124  # Replace with your department server ID
CHANNEL_ID = 1416912156569636985  # Replace with the channel ID for logs
DEPARTMENT_LOGO = "https://cdn.discordapp.com/attachments/1400670794232631369/1402316853040124014/image.png?ex=68cd7ad7&is=68cc2957&hm=a0b39324d93817bf46838e1c3eed87ddfd93089adb2dffbdaabe2a7e90188503&"
COLOR_SCHEME = 0x8A8A8A  # Department gray


class OfficerLoggerCog(commands.Cog):
    """Logs officer join/leave events for the department."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id != GUILD_ID:
            return

        channel = member.guild.get_channel(CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                description=(
                    f"{member.mention} has joined the department. "
                    f"We now have **{len(member.guild.members)}** members."
                ),
                color=COLOR_SCHEME,
                timestamp=datetime.now(timezone.utc)
            )
            embed.set_author(name="Senora Valley Police Department", icon_url=DEPARTMENT_LOGO)
            embed.set_thumbnail(url=DEPARTMENT_LOGO)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id != GUILD_ID:
            return

        channel = member.guild.get_channel(CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                description=(
                    f"{member.mention} has left the department. "
                    f"We now have **{len(member.guild.members)}** members."
                ),
                color=COLOR_SCHEME,
                timestamp=datetime.now(timezone.utc)
            )
            embed.set_author(name="Senora Valley Police Department", icon_url=DEPARTMENT_LOGO)
            embed.set_thumbnail(url=DEPARTMENT_LOGO)
            await channel.send(embed=embed)


# ------------------------------
# SETUP
# ------------------------------
async def setup(bot: commands.Bot):
    await bot.add_cog(OfficerLoggerCog(bot))
