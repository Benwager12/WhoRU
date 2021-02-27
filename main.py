###########################################
# WhoRU Discord Bot
# See which celebrity you look like!
###########################################

from recognise_face import lookup
from os import remove

###########################################
# Loading variables
###########################################
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX")

###########################################
# Initialising discord bot
###########################################
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = PREFIX)

@bot.event
async def on_ready():
	print("Bot is online")

###########################################
# Comamnds
###########################################

image_types = ["png", "jpeg", "jpg"]

@bot.command()
async def who(ctx):
	if len(ctx.message.attachments) == 0:
		return await ctx.reply("No attachments given.")

	# Iterating through attachments and saving them, deleting later.
	for attachment in ctx.message.attachments:
		if not attachment.filename.lower().split(".")[-1] in image_types:
			continue
		await attachment.save("temporary-images/" + attachment.filename)

	# Iterating through attachments and saying who it looks like
	for attachment in ctx.message.attachments:
		name = lookup("temporary-images/" + attachment.filename)

		if name == None:
			return await ctx.reply("No faces in image.")
			continue
		elif name == ">1":
			await ctx.reply("More than 1 face in image.")
			continue
		else:
			await ctx.reply("The picture you sent (apparently) looks like " + name)

	# Deleting attachments.
	for attachment in ctx.message.attachments:
		remove("temporary-images/" + attachment.filename)

###########################################
# Inserting token
###########################################
bot.run(DISCORD_TOKEN)
