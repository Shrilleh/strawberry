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

        self.cached_messages = []  # store preloaded messages
        self.target_channel_id = 1212444252995592275  # FMERAL CHANNEL ID

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_guess_messages()
        print(f"loaded {len(self.cached_messages)} messages")

    # load and cache message on start up (faster retrieval)
    async def load_guess_messages(self):
        channel = self.bot.get_channel(self.target_channel_id)
        if channel is None:
            return

        cutoff = datetime.now(timezone.utc) - timedelta(days=60)
        messages = []

        async for msg in channel.history(limit=3000, after=cutoff):
            if msg.author.bot:
                continue
            if not msg.content or len(msg.content.strip()) < 6:
                continue
            if any(ext in msg.content.lower() for ext in [".gif", ".png", ".jpg", ".jpeg", "http://", "https://"]):
                continue
            
            messages.append(msg)

        self.cached_messages = messages


    @commands.command()
    async def guessmsg(self, ctx):
        # make sure same channel
        if not isinstance(ctx.channel, discord.TextChannel):
            return
        if not self.cached_messages:
            await self.load_guess_messages()  # fallback if not loaded yet
        if not self.cached_messages:
            return

        # get random message from cached messages
        target_msg = random.choice(self.cached_messages)
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
    
    @commands.command()
    async def guessword(self, ctx):
        if not self.cached_messages:
            await self.load_guess_messages()  # fallback if not loaded yet

        if not self.cached_messages:
            return

        # get random message
        target_msg = random.choice(self.cached_messages)
        target_author = target_msg.author
        words = target_msg.content.split() # get words in message

        # pick a random word and hide it
        hidden_index = random.randrange(len(words))
        hidden_word = words[hidden_index]
        masked_words = words.copy()
        masked_words[hidden_index] = "_" * len(hidden_word) # make it _ the length of the word

        await ctx.send(
            "fill in the blank:\n"
            f"```{' '.join(masked_words)}```"
        )

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            guess_msg = await self.bot.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(
                f"it was **{hidden_word}** "
                f"by **{target_author.display_name}**"
            )
            return

        # what the user guesses vs real word
        guess_text = guess_msg.content.strip().lower()
        real_word = hidden_word.lower()

        # if guess right vs wrong
        if guess_text == real_word:
            await ctx.send(
                f"correct: **{target_author.display_name}** said:\n"
                f"```{target_msg.content}```"
            )
        else:
            await ctx.send(
                f"it was **{hidden_word}** "
                f"by **{target_author.display_name}**\n"
                f"```{target_msg.content}```"
            )

async def setup(bot):
    await bot.add_cog(Guess(bot))
