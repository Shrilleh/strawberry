
from discord.ext import commands
from gtts import gTTS
import discord
import os
import uuid

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ensure_voice(self, ctx):
        voice = ctx.voice_client
        if ctx.author.voice:
            channel = ctx.author.voice.channel

        else:
            default_channel = "sleepy time"
            channel = discord.utils.get(ctx.guild.voice_channels, name=default_channel)
            
            if channel is None:
                await ctx.send("cant find channel")
                return None

        # connect to channel
        if voice is None:
            voice = await channel.connect()
        elif voice.channel != channel:
            await voice.move_to(channel)

        return voice

    @commands.command()
    async def speaky(self, ctx, *, text: str):
        # get voice
        voice = await self.ensure_voice(ctx)
        if voice is None:
            return

        # create temp file to play
        filename = f"tts_{uuid.uuid4().hex}.mp3"

        prefix = "Hi guys strawb here, "
        tts = gTTS(text=prefix + text, lang="en")
        tts.save(filename)

        source = discord.FFmpegPCMAudio(filename)

        def after_playing(error):
            try:
                os.remove(filename)
            except OSError:
                pass

        voice.play(source, after=after_playing)

    # disconnect bot
    @commands.command()
    async def leavevc(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("not in channel twyn")

async def setup(bot):
    await bot.add_cog(TTS(bot))
