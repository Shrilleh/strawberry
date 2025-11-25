# DO NOT EDIT OR DELETE - FOR SHOWING PURPOSE
from discord.ext import commands
import discord

"""
For regular commands (i.e used with prefix) use: @commands.command() BEFORE defining a function
For bot events (i.e on_message, on_member_join) use @commands.Cog.listener() BEFORE defining a function

In the examples below (step-by-step):
1. Defines a class
    - A Cog class is a component of the bot features
    - Can have multiple cogs, this one below called 'Example' or 'Music' etc.

2. Initalize class 
    - self.bot stores reference to the bot

3. Use decorator to defin comamnd
    -   @commands.command() for prefix (i.e !ping)
    -   @commands.Cog.listener() for discod event (i.e someone send messgae (on_message))

4. define async (run parallel) functions - ONE Function for EACH command

5. function recieve CONTEXT (ctx) argument
    - it got stuff like who sent command, what channel etc.
    - helpful function like ctx.send for bot send a message

6. fmychudlife
"""

class Example(commands.Cog):
    # Class of example commands

    def __init__(self, bot):
        self.bot = bot

    # REPLY PING TO PONG
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
    # FOR EXAMPLE: 
    # kitten: !ping
    # straw: Pong!

    # REPEAT WHAT USER SENDS
    @commands.command()
    async def say(self, ctx, *, message: str):
        
        await ctx.send(message)
    # FOR EXAMPLE: 
    # kitten: !say bro
    # straw: bro

    # FOR BOT EVENTS (i.e on_message) use @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore bots own messages
        if message.author == self.bot.user:
            return

        # If user messages "testbot"
        if "testbot" in message.content.lower():
            await message.channel.send(f"{message.author.mention} Hi, bot working!") # Mentions user, messages back

async def setup(bot):
    await bot.add_cog(Example(bot))
