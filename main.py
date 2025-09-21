# main.py
import discord
from discord.ext import commands
import os, asyncio, logging
from dotenv import load_dotenv
from threading import Thread
from flask import Flask

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.getenv("PORT", 5000))  # For hosting services

# Bot Settings
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True
INTENTS.guilds = True

PREFIX = "!"
COLOR = discord.Color(int("8a8a8a", 16))  # #8a8a8a
LOGO_URL = "https://cdn.discordapp.com/attachments/1231290151708131379/1403809096544813109/Untitled_design__3_-removebg-preview.png?ex=68c9ae1a&is=68c85c9a&hm=a885942430a9f12904a8aa0695e9bdad5af427377c3f7d5c0d9f3788b994678b&"

# ---------------- Discord Bot ----------------
class DepartmentBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=INTENTS)
        self.color = COLOR
        self.logo = LOGO_URL

    async def setup_hook(self):
        # Auto-load cogs in the "cogs" folder
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"Loaded cog: {filename}")
                except Exception as e:
                    print(f"Failed to load cog {filename}: {e}")

        # Sync slash commands globally
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands globally")
        except Exception as e:
            print(f"Command sync failed: {e}")

    async def on_ready(self):
        print(f"\nBot is online as {self.user} (ID: {self.user.id})")
        print("------")

# ---------------- Flask Server ----------------
app = Flask("DepartmentBot")

@app.route("/")
def home():
    return "Bot is running ✅", 200

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

# ---------------- Logging setup ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

bot = DepartmentBot()

# ---------------- Run both ----------------
if __name__ == "__main__":
    # Run Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run Discord bot
    asyncio.run(bot.start(TOKEN))
