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
        self.image_messages = []  # list of (message, image_url)
        self.target_channel_id = 1212444252995592275  # FMERAL CHANNEL ID

    def guess_member(self, guild: discord.Guild, guess_text: str) -> discord.Member | None:
        guess_text = guess_text.strip().lower()
        if not guess_text:
            return None

        # exact username or display name match
        for member in guild.members:
            if member.name.lower() == guess_text or member.display_name.lower() == guess_text:
                return member

        # alias match
        for user_id, alias_list in self.aliases.items():
            for alias in alias_list:
                if guess_text == alias.lower():
                    member = guild.get_member(user_id)
                    if member is not None:
                        return member

        return None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_guess_messages()
        await self.load_image_messages()
        print(f"loaded {len(self.cached_messages)} messages")

    # load and cache message on start up (faster retrieval)
    async def load_guess_messages(self):
        channel = self.bot.get_channel(self.target_channel_id)
        if channel is None:
            return

        cutoff = datetime.now(timezone.utc) - timedelta(days=90)
        messages = []

        async for msg in channel.history(limit=5000, after=cutoff):
            if msg.author.bot:
                continue
            if not msg.content or len(msg.content.strip()) < 6:
                continue
            if any(ext in msg.content.lower() for ext in [".gif", ".png", ".jpg", ".jpeg", "http://", "https://"]):
                continue
            
            messages.append(msg)

        self.cached_messages = messages

    async def load_image_messages(self):
        """Preload image messages for guessimg."""
        channel = self.bot.get_channel(self.target_channel_id)
        if channel is None:
            print("[Guess] image channel not found")
            return

        cutoff = datetime.now(timezone.utc) - timedelta(days=90)
        images = []

        async for msg in channel.history(limit=2000, after=cutoff):
            if msg.author.bot:
                continue
            if not msg.attachments:
                continue

            # keep only image attachments
            image_attachments = [
                a for a in msg.attachments
                if (a.content_type and a.content_type.startswith("image/"))
                or a.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
            ]

            if not image_attachments:
                continue

            # just take the first image for this message
            images.append((msg, image_attachments[0].url))

        self.image_messages = images
        print(f"loaded {len(self.image_messages)} images (urls)")



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
            await ctx.send(f"it was **{target_author.display_name}**\n"
                           f"<{target_msg.jump_url}>")
            return

        guessed_member = self.guess_member(ctx.guild, guess_msg.content)

        if not guessed_member:
            return  

        if guessed_member.id == target_author.id:
            await ctx.send(f"correct: **{target_author.display_name}**\n"
                           f"<{target_msg.jump_url}>")
        else:
            await ctx.send(f"nope answer was: **{target_author.display_name}**\n"
                           f"<{target_msg.jump_url}>")
    
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
                f"by **{target_author.display_name}**\n"
                f"<{target_msg.jump_url}>"
            )
            return

        # what the user guesses vs real word
        guess_text = guess_msg.content.strip().lower()
        real_word = hidden_word.lower()

        # if guess right vs wrong
        if guess_text == real_word:
            await ctx.send(
                f"correct: **{target_author.display_name}** said:\n"
                f"```{target_msg.content}```\n"
                f"<{target_msg.jump_url}>"
            )
        else:
            await ctx.send(
                f"it was **{hidden_word}** "
                f"by **{target_author.display_name}**\n"
                f"```{target_msg.content}```\n"
                f"<{target_msg.jump_url}>"
            )

    # GUESS IMAGE
    @commands.command()
    async def guessimg(self, ctx):
        # load cache if empty
        if not self.image_messages:
            await self.load_image_messages()

        if not self.image_messages:
            print("fail")
            return

        #random image get
        target_msg, image_url = random.choice(self.image_messages)
        target_author = target_msg.author

        await ctx.send("who sent this image?")
        await ctx.send(image_url)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            guess_msg = await self.bot.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"it was **{target_author.display_name}**")
            return

        guessed_member = self.guess_member(ctx.guild, guess_msg.content)

        if not guessed_member:
            return

         # if right or wrong
        if guessed_member.id == target_author.id:
            await ctx.send(f"correct: **{target_author.display_name}**\n"
                           f"<{target_msg.jump_url}>")
        else:
            await ctx.send(f"nope answer was: **{target_author.display_name}**\n"
                           f"<{target_msg.jump_url}>")

    
async def setup(bot):
    await bot.add_cog(Guess(bot))
