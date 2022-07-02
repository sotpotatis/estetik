'''error_handling.py
Discord Bot error handling.
'''
from discord.ext import commands
from util import generate_error_embed
import logging, traceback, sys, asyncio

class ErrorHandlingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''Handles an error raised by the bot'''
        IGNORED_ERRORS = (commands.CommandNotFound,)
        if isinstance(error, IGNORED_ERRORS):
            self.logger.debug("Ignoring raised error, is invalid command...")
            return
        elif isinstance(error, asyncio.TimeoutError):
            self.logger.info("The user was too slow. Returning error...")
            await ctx.send(embed=generate_error_embed(
                "Timeout",
                "There is a timeout on the question that the bot was waiting for an answer to. Can't wait all day, you know? Please try invoking the command again."
            ))
            return

        self.logger.critical("Handling an error raised by the bot!")
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        error = getattr(error, "original", error) #Get original error
        error_embed = generate_error_embed(
            "An unhandled error occurred",
            "Sorry, an unknown error occurred. Here is some information:",
            fields=[{
                "name": "Details",
                "value": f"The error was: `{error}` (type: `{str(type(error))}`).",
                "inline": False
            }]
        )
        await ctx.send(embed=error_embed)