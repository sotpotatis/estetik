from discord.ext import commands
from other_commands import OtherCommands
from basic_commands import BasicCommands
from error_handling import ErrorHandlingCog
from automation.python_api_client.api_client import *

#Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

#Bot
discord_token = os.environ["ESTETIK_BOT_TOKEN"]
bot = commands.Bot(command_prefix="es ")
#Bot commands
bot.add_cog(BasicCommands(bot))
bot.add_cog(OtherCommands(bot))
bot.add_cog(ErrorHandlingCog(bot))
#Bot events
@bot.event
async def is_ready(*args, **kwargs):
    logger.info("Bot is logged in and ready!")
bot.run(discord_token)