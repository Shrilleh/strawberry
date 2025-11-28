
# DON'T EDIT THIS FILE UNLESS NECESSARY

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import asyncio


# Get token
load_dotenv()
token = os.getenv("token")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') # logging and debugging
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# INITIALIZE BOT - DEFINE PREFIX 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Ready to go {bot.user.name}")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

async def load_components():
    components_directory = os.path.join(os.path.dirname(__file__), "components")
    for filename in os.listdir(components_directory):
        if filename.endswith(".py") and not filename.startswith("_"):
            component_name = filename[:-3]  # strip .py
            extension = f"components.{component_name}"
            try:
                await bot.load_extension(extension)
                print(f"Loaded component: {extension}")
            except Exception as e:
                print(f"Failed to load component {extension}: {e}")

# TURN BOT ON
async def main():
    await load_components()
    logging.basicConfig(handlers=[handler], level=logging.DEBUG)
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())