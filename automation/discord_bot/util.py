'''util.py
Various utilities related to the discord bot.'''
from discord import Embed
from automation.discord_bot.bot_const import EMBED_COLOR_ERROR
import logging
logger = logging.getLogger(__name__)

def generate_error_embed(error_title, error_description, fields=None):
    '''Creates an error embed message that indicates what has gone wrong.

    :param error_title: A title for the error. The text "Error:" will be added to the beginning of it.

    :param error_description: A description what went wrong.

    :param fields: A list of fields to add to the embed: [{"name": "<name>", "value": "<value>"}]'''
    logger.debug(f"Generating an error embed for the title: {error_title} and the description: {error_description}...")
    embed = Embed(
        title=f"Error: {error_title}",
        description=error_description,
        color=EMBED_COLOR_ERROR
    )
    if fields != None:
        logger.debug("Adding field(s) to error embed...")
        for field in fields:
            embed.add_field(**field)
    return embed