'''basic_commands.py
The commands that power the bot.
Welcome!'''
import logging, os, time, platform, psutil
from discord.ext import commands
from discord import Embed, Color
from bot_const import EMBED_COLOR
from pathlib import Path
from tempfile import mkstemp
from automation.python_api_client.api_client import Client
from util import generate_error_embed

IMAGE_FILE_EXTENSIONS = [".png", ".jpg", ".gif"]


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.api_domain = os.getenv("ESTETIK_API_DOMAIN")
        self.use_ssl = (os.getenv("ESTETIK_SSL") == True) if os.getenv("ESTETIK_SSL") != None else True
        if self.use_ssl:
            self.logger.info("SSL will be used for connections.")
        else:
            self.logger.warning("SSL has been disabled! Please use it in a production environment.")
        self.estetare_client = Client(os.environ["ESTETIK_TOKEN"],
                             api_domain=self.api_domain,
                             use_https=self.use_ssl)
        self.current_ctx = None
        self.reaction_emojis_waited_for = []
        self.not_acknowledged_error_message = generate_error_embed(
            "No response",
            "I did not get a response from you within the timeout (60s). Please try again."
        ) #Error message to send when the bot did not get an answer to its message


    def attachment_image(self, message):
        '''Waits for an image attachment.'''
        if message.author == self.current_ctx.author:
            self.logger.debug("Checking for image in message by original author...")
            if len(message.attachments) > 0:
                self.logger.debug("Attachments included in message!")
                file_extension = Path(message.attachments[0].filename).suffix.lower()
                self.logger.debug(f"Attachment has file extension: {file_extension}. Allowed file extensions are: {IMAGE_FILE_EXTENSIONS}")
                return file_extension in IMAGE_FILE_EXTENSIONS
            else:
                self.logger.debug("No attachments were included in the message")
    def is_message_from_author(self, message):
        '''Waits for a message from the command invoke author'''
        return message.author == self.current_ctx.author

    def wait_for_reaction(self, reaction, user):
        '''Waits for a reaction by the original user.'''
        return (reaction.emoji in self.reaction_emojis_waited_for and user == self.current_ctx.author)
    @commands.command(description="Adds an image to the server")
    @commands.is_owner()
    async def add_image(self, ctx):
        self.current_ctx = ctx
        self.logger.info("Got a request to add an image to the server!")
        #Some pre-stuff
        #First, send a confirmation message
        await ctx.send(embed=Embed(
            title="I hear you!",
            description="Now, please, post the image that you want.",
            color=EMBED_COLOR
        ))
        image_request = await self.bot.wait_for("message", check=self.attachment_image, timeout=60)
        if image_request == None:
            self.logger.warning("Did not receive an image!")
            await ctx.send(embed=self.not_acknowledged_error_message)
            return
        self.logger.info("Received an image. Keeping track of it...")
        image_file_stream, sent_image_path = mkstemp(suffix=Path(image_request.attachments[0].filename).suffix.lower())
        await image_request.attachments[0].save(sent_image_path)
        self.logger.info("Image saved.")
        #Now, get other things as required
        #Part ID
        defined_parts = self.estetare_client.get_segment_structure_for("images")["content"]["parts"]
        DEFINED_PART_IDS = [part["id"] if "id" in part else None for part in defined_parts] #Get which part IDs that have already been defined
        part_id_embed = Embed(
            title="What part/collection do you want to add this to?",
            description="To freshen your mind up, here is a list of the parts that are available: \n{}".format(
                "\n".join([f"* `{part_id}`" for part_id in DEFINED_PART_IDS])
            ),
            color=EMBED_COLOR
        )
        await ctx.send(embed=part_id_embed)
        belongs_to_part_id_request = await self.bot.wait_for("message", check=self.is_message_from_author, timeout=60)
        if belongs_to_part_id_request == None:
            self.logger.warning("Did not receive a part ID!")
            await ctx.send(embed=self.not_acknowledged_error_message)
            return
        belongs_to_part_id = belongs_to_part_id_request.content
        if belongs_to_part_id not in DEFINED_PART_IDS:
            self.logger.warning("Invalid part ID!")
            await ctx.send(embed=generate_error_embed(
                "Invalid part ID",
                f"You entered an invalid part ID. The Part ID must be one of the following: `{','.join(DEFINED_PART_IDS)}`, but you said `{belongs_to_part_id}`."
            ))
            return
        #...and get the image title...
        await ctx.send(embed=Embed(
            title="Image title time!",
            description="Enter the title of the image.",
            color=EMBED_COLOR
        ))
        image_title_request = await self.bot.wait_for("message", check=self.is_message_from_author, timeout=60)
        if image_title_request == None:
            self.logger.warning("Did not receive an image title!")
            await ctx.send(embed=self.not_acknowledged_error_message)
            return
        image_title = image_title_request.content
        #Generate an image ID based on the title. This will also decide the final filename on the server
        image_id = image_title.replace(" ", "_").lower()
        #...and the image description...
        await ctx.send(embed=Embed(
            title="Add a description!",
            description="Put in a description for the image.",
            color=EMBED_COLOR
        ))
        image_description_request = await self.bot.wait_for("message", check=self.is_message_from_author, timeout=60)
        if image_description_request == None:
            self.logger.warning("Did not get an image description!")
            await ctx.send(embed=self.not_acknowledged_error_message)
            return
        image_description = image_description_request.content
        #And upload
        self.logger.info("Uploading. Sending information message...")
        confirmation_embed = Embed(
            title="Uploading file...",
            description="The file is now being uploaded to the server.",
            color=Color.blue()
        )
        image_text_information = f"""
        **Title:** `{image_title}`
        **Description:** `{image_description}`.
        **Assigned ID:** `{image_id}`
        **Uploading to part:** `{belongs_to_part_id}`
        **Image local path:** `{sent_image_path}`
        """ #Some text information about the image
        confirmation_embed.add_field(name="Information", value=image_text_information, inline=False)
        confirmation_message = await ctx.send(embed=confirmation_embed)
        request_time = time.time()
        self.estetare_client.create_new_image_item(
            image_path=sent_image_path, image_title=image_title, image_description=image_description, image_id=image_id, belongs_to_part_id=belongs_to_part_id
        )
        self.logger.info("Image created.")
        request_time = time.time() - request_time
        confirmation_embed = Embed(
            title="File uploaded!",
            description="The file has now been uploaded to the Estetare media management API.",
            color=Color.green()
        )
        confirmation_embed.add_field(name="Details", value=f"The request took {round(request_time, 2)} seconds. {image_text_information}", inline=False)
        await confirmation_message.edit(embed=confirmation_embed)
        self.logger.info("Done with file uploading process.")

    @commands.command(description="Allows to add a part")
    @commands.is_owner()
    async def add_part(self, ctx):
        '''Allows you to add a part. A part is a way to sort images.'''
        self.logger.info("Got a request to add a part!")
        #Acknowledge and start collecting information
        self.current_ctx = ctx

        await ctx.send(embed=Embed(
            title="I hear you!",
            description="Time to fill out some details, starting with the **title** of the part.",
            color=EMBED_COLOR
        ))
        title_request = await self.bot.wait_for("message", check=self.is_message_from_author, timeout=60)
        if title_request == None:
            self.logger.warning("Did not receive a title!")
            await ctx.send(embed=self.not_acknowledged_error_message)
            return
        title = title_request.content
        part_id = title.replace(" ", "_") #Generate part ID based on title
        await ctx.send(
            embed=Embed(
                title="Description?",
                description="Please answer with the **description** that you want this part to have.",
                color=EMBED_COLOR
            )
        )
        description_request = await self.bot.wait_for("message", check=self.is_message_from_author, timeout=60)
        if description_request == None:
            self.logger.warning("Did not receive a description!")
            await ctx.send(embed=self.not_acknowledged_error_message)
        description = description_request.content
        #Ask where to create the new part
        part_options = {
            "1️⃣": "images",
            "2️⃣": "text",
            "3️⃣": "music",
        }
        part_options_message = await ctx.send(embed=Embed(
            title="Where should this part be created?",
            description=f"Pick an option from below: \n%s"%('\n'.join([emoji + ' - ' + parent_id for emoji, parent_id in part_options.items()])), #I love oneliners but PEP doesn't :((
            color=EMBED_COLOR
        ))
        self.reaction_emojis_waited_for = list(part_options.keys())
        for emoji in part_options.keys():
            await part_options_message.add_reaction(emoji)
        reacted_emoji, reacted_by = await self.bot.wait_for("reaction_add", check=self.wait_for_reaction, timeout=60)
        if reacted_emoji == None:
            self.logger.warning("Did not get a response on where to create the part!")
            await ctx.send(embed=self.not_acknowledged_error_message)
            return
        where_to_create_part = part_options[str(reacted_emoji.emoji)]
        ctx.send(embed=generate_error_embed("Internal error", "Could not extract reaction. Please try again. If the issue persists, there might be something wrong with the source code."))
        self.logger.info("Got where to create a part.")
        #Send confirmation message
        confirmation_embed = Embed(
            title="Creating...",
            description="The new part will now be created.",
            color=EMBED_COLOR
        )
        confirmation_embed.add_field(
            name="Details",
            value=f"Creating part in `{where_to_create_part}` with ID `{part_id}`, title `{title}` and description `{description}`.",
            inline=False
        )
        confirmation_message = await ctx.send(embed=confirmation_embed)
        request_time = time.time()
        self.logger.info("Sending request to create new part...")
        self.estetare_client.create_new_part(media_type_to_create_part_in=where_to_create_part,
                                             part_id=part_id,
                                             part_title=title,
                                             part_description=description,
                                             part_segments=[]) #Create part with empty segments from the beginning
        self.logger.info("Request sent. Editing original message...")
        confirmation_embed = Embed(
            title="Created!",
            description="The part has now been created.",
            color=EMBED_COLOR
        )
        request_time = time.time() - request_time
        confirmation_embed.add_field(name="Details", value=f"The request took {round(request_time, 2)} seconds.")
        await confirmation_message.edit(embed=confirmation_embed)
        self.logger.info("All done, the part has been created.")

    @commands.command(description="Shows some statistics and information about the bot")
    @commands.is_owner()
    async def botinfo(self, ctx):
        '''Command to show some basic information about the bot, such as connection information.'''
        self.logger.info("Got a request to the bot-info command. Returning information...")
        information_embed = Embed(
            title="Information",
            description="Below are some information about how the bot is connected.",
            color=Color.blue()
        )
        information_embed.add_field(name="Server information",
                                    value=f"""
                                    **Server URL:** `{self.api_domain}`
                                    **HTTPS:** `{self.use_ssl}`""",
                                    inline=False)
        information_embed.add_field(name="Discord information",
                                    value=f"**Ping:** `{round(self.bot.latency, 1)}` ms",
                                    inline=False)
        information_embed.add_field(name="OS information",
                                    value=f"""**Platform:**  `{platform.platform()}`
                                    **CPU:** `{platform.processor()}` 
                                    **Architecture:** (`{platform.architecture()}`)
                                    **CPU usage:** `{psutil.cpu_percent()}%`
                                    **RAM usage:** `{psutil.virtual_memory().percent}%`""",
                                    inline=False)
        await ctx.send(embed=information_embed)
        self.logger.info("Bot info sent.")