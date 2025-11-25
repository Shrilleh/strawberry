
# COPY PASTE THIS FILE , then edit

from discord.ext import commands
import discord

class Fun(commands.Cog):
    # Class of fun commands

    def __init__(self, bot):
        self.bot = bot

    # REPLY DING TO DONG
    @commands.command()
    async def ding(self, ctx):
        await ctx.send("Dong!")
    # FOR EXAMPLE: 
    # kitten: !ding
    # straw: Dong!

    # REPEAT WHAT USER SENDS
    @commands.command()
    async def speak(self, ctx, *, message: str):
        await ctx.send(message)
    # FOR EXAMPLE: 
    # kitten: !speak bro
    # straw: bro

# Setup component (ensure you adding the correct class)
async def setup(bot):
    await bot.add_cog(Fun(bot))