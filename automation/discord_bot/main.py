#The API client path should be specified in an argument, api_client_path, that should be passed to the bot.
import sys
from argparse import ArgumentParser
import pathlib
parser = ArgumentParser(description="Runs a Discord management bot for the Estetik API.")
parser.add_argument("api_client_path", type=pathlib.Path)
passed_args = parser.parse_args()
api_client_path = passed_args.api_client_path
print(f"Loading API client from {api_client_path}...")
from api_client import *
sys.path.append(str(api_client_path))
from discord.ext import commands
from other_commands import OtherCommands
from basic_commands import BasicCommands
from error_handling import ErrorHandlingCog
import logging, os

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