# DO NOT EDIT OR DELETE - FOR SHOWING PURPOSE
from discord.ext import commands
import discord,random


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
samSentences = ["", "Shut up you stinky winston lover", "you are bad at siege","hi pookie","quit yapping","have sex with ryan gawenda NOW","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]


class Gawenda(commands.Cog):
    # Class of example commands

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore bots own messages
        if message.author == self.bot.user:
            return

        
        if message.author.name == "bagelboi4000":
         pick = random.choice(samSentences)
        await message.channel.send(pick)

async def setup(bot):
    await bot.add_cog(Gawenda(bot))
