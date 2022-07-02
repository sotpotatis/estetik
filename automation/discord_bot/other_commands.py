import logging
from discord import Embed
from discord.ext import commands
from automation.discord_bot.bot_const import EMBED_COLOR
logger = logging.getLogger(__name__)

class OtherCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        logger.info("Got a request to the ping command.")
        message = Embed(
            title="Pong!",
            description=f"I'm swaggin' around at {round(self.bot.latency, 1)} ms latency.",
            color=EMBED_COLOR
        )
        await ctx.send(embed=message)
