
# COPY PASTE THIS FILE , then edit

from discord.ext import commands
import discord

class Fun(commands.Cog):
    # Class of fun commands

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

# Setup component (ensure you adding the correct class)
async def setup(bot):
    await bot.add_cog(Fun(bot))