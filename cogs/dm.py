# cogs/dm_tools.py
import discord
from discord.ext import commands
from discord import app_commands, ui
from datetime import datetime

class DMModal(ui.Modal, title="Send a DM"):
    def __init__(self, officer: discord.Member):
        super().__init__(timeout=None)
        self.officer = officer
        self.statement = ui.TextInput(
            label="DM",
            style=discord.TextStyle.paragraph,
            placeholder="Type the DM you want to send...",
            required=True,
            max_length=2000
        )
        self.add_item(self.statement)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="We'd like to get in contact,",
            description=self.statement.value,
            color=0x8a8a8a
        )

        view = DMConfirmView(self.officer, embed)
        await interaction.response.send_message(
            content="Here’s the preview. Press **Send** to deliver:",
            embed=embed,
            view=view,
            ephemeral=True
        )


class DMConfirmView(ui.View):
    def __init__(self, officer: discord.Member, embed: discord.Embed):
        super().__init__(timeout=180)
        self.officer = officer
        self.embed = embed

    @ui.button(label="Send", style=discord.ButtonStyle.secondary)
    async def send_button(self, interaction: discord.Interaction, button: ui.Button):
        try:
            await self.officer.send(embed=self.embed)
            await interaction.response.edit_message(
                content=f"Message successfully sent to {self.officer.mention}.",
                embed=None,
                view=None
            )
        except discord.Forbidden:
            await interaction.response.edit_message(
                content=f"Could not DM {self.officer.mention} (their DMs may be closed).",
                embed=None,
                view=None
            )


class DMTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dm", description="Send a DM to an officer via form")
    async def dm(self, interaction: discord.Interaction, officer: discord.Member):
        modal = DMModal(officer)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="hire", description="Hire an officer and send them a welcome DM")
    async def hire(self, interaction: discord.Interaction, officer: discord.Member):
        invite = await interaction.guild.text_channels[0].create_invite(
            max_uses=1, unique=True
        )

        embed = discord.Embed(
            title="Welcome to the department,",
            description=(
                f"Congratulations on passing the Senora Valley Police Department's application. "
                f"Your application was reviewed at {datetime.utcnow().strftime('%B %d, %Y %I:%M %p UTC')}.\n\n"
                "You will be given an invite link. This is a security measure, these codes cannot be shared, "
                "displayed or re-used. If attempted, you will be automatically removed by our systems.\n\n"
                "You must complete your training process within 3 weeks. If you require an extension, "
                "create a support ticket by messaging this bot.\n\n"
                f"Invite link: ||{invite.url}||\n\n"
                "With kind regards,"
            ),
            color=0x8a8a8a
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1400670794232631369/1402316853040124014/image.png?ex=68cd7ad7&is=68cc2957&hm=a0b39324d93817bf46838e1c3eed87ddfd93089adb2dffbdaabe2a7e90188503&"
        )

        try:
            await officer.send(embed=embed)
            await interaction.response.send_message(
                f"Sent hire message to {officer.mention}.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                f"Could not DM {officer.mention} (their DMs may be closed).",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(DMTools(bot))
