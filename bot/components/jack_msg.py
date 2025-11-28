from discord.ext import commands
import discord
import random
import asyncio
from datetime import datetime, timedelta, timezone

class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = [] # initalize message history
        
        # each perosn id - mapped to list of possible alias (u can add names)
        self.aliases = {
            247471730661130243 : ['alvis'],
            269894939691712514 : ['jack'],
            371760411051163649 : ['wren'],
            382552535912677389 : ['sam'],
            425363947093229589 : ['gawenda'],
            630365991804862474 : ['ollie'],
            699619182672871506 : ['hana'],
            861282807824908298 : ['niall']
        }


    @commands.command()
    async def guessmsg(self, ctx):

        # make sure same channel
        if not isinstance(ctx.channel, discord.TextChannel):
            return

        # get date cutoff (30 days rn)
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)

        # get message history (currently only in current channel - quicker ways to do this (i.e load messages on bot start))
        async for msg in ctx.channel.history(limit=1000, after=cutoff):
            if msg.author.bot: # don't include bot msg
                continue
            if not msg.content or len(msg.content.strip()) < 5: # only real/longer message 
                continue
            self.messages.append(msg)

        if not self.messages:
            return

        # get rando message, and its author
        target_msg = random.choice(self.messages)
        target_author = target_msg.author

        await ctx.send(
            "who said:\n"
            f"```{target_msg.content}```\n"
        )

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            # check for message (by person we request the !guessmsg (for now !)) TIMEOUT if NO ANSWER
            guess_msg = await self.bot.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"it was **{target_author.display_name}**")
            return

        # initalized guess & get text from message
        guessed_member = None
        guess_text = guess_msg.content.strip().lower()

        # loop through members, check if user or nick name match
        for member in ctx.guild.members:
            if member.name.lower() == guess_text or member.display_name.lower() == guess_text:
                guessed_member = member
                break

        # alias match (only if not discord name given)
        if guessed_member is None:
            for user_id, alias_list in self.aliases.items():
                for alias in alias_list:
                    if guess_text == alias.lower():
                        member = ctx.guild.get_member(user_id)
                        if member:
                            guessed_member = member
                        break
                if guessed_member is not None:
                    break

        # no one guessed
        if not guessed_member:
            return

        # if answer right
        if guessed_member.id == target_author.id:
            await ctx.send(f"correct: **{target_author.display_name}**") # right answer
        else:
            await ctx.send(f"nope answer was: **{target_author.display_name}**") # if answer wrong

async def setup(bot):
    await bot.add_cog(Guess(bot))
