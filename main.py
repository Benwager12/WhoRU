###########################################
# WhoRU Discord Bot
# See which celebrity you look like!
###########################################

from recognise_face import lookup
from os import remove

###########################################
# UUID Generator
###########################################
from random import randint

alphabet = "abcdefghiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

def uuid_char():
	# Get a random character in the alphabet string.
	return alphabet[randint(0, len(alphabet)-1)]

def make_uuid(length=16):
	# Join a bunch of characters of the length variable length.
	# Those characters are called individually from the method "uuid_char"
	return "".join([uuid_char() for x in range(length)])

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

	# Dictionary which contains the array of files to their respective UUID.
	filesToUUID = {}

	# Iterating through attachments and saving them, deleting later.
	for attachment in ctx.message.attachments:
		if not attachment.filename.lower().split(".")[-1] in image_types:
			continue

		extension = "."+attachment.filename.split(".")[-1]
		uuid = make_uuid()

		filesToUUID[attachment.filename] = uuid+extension
		await attachment.save(f"temporary-images/{uuid}{extension}")

	# Iterating through attachments and saying who it looks like
	for file in filesToUUID.keys():
		name = lookup("temporary-images/" + filesToUUID[file])

		if name == None:
			await ctx.reply("No faces in image.")
		elif name == ">1":
			await ctx.reply("More than 1 face in image.")
		else:
			face_file = discord.File("faces/"+name+".jpg")
			await ctx.reply("The picture you sent (apparently) looks like " + name, file=face_file)
		
		# Delete the attachment after I'm finished with it.
		remove("temporary-images/" + filesToUUID[file])

###########################################
# Inserting token
###########################################
bot.run(DISCORD_TOKEN)
