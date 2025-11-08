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
COLOR = discord.Color(int("E7BB19", 16))  # #E7BB19
LOGO_URL = "https://media.discordapp.net/attachments/1400897643772907640/1424180413076606977/Untitled_design_4.png?ex=69107e9e&is=690f2d1e&hm=74989a85019ed50ac5814b2ce101c204b3f26cfe13a3d62351af0d34c5e76cad&=&format=webp&quality=lossless"

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
    return "Bot is running", 200

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
