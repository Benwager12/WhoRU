#!/usr/bin/python3.9

###########################################
# WhoRU Discord Bot
# See which celebrity you look like!
###########################################

from recognise_face import lookup
from os import remove, getenv
from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord import File
from random import choice, sample
from string import ascii_letters, digits

alphabet = ascii_letters + digits

image_types = ["png", "jpeg", "jpg"]

load_dotenv()
if not (DISCORD_TOKEN := getenv("DISCORD_TOKEN")):
	DISCORD_TOKEN = input(
		" Assign DISCORD_TOKEN as environment variable\n Input now for a try>")

PREFIX = getenv("PREFIX")
if not (PREFIX := getenv("PREFIX")):
	PREFIX = input(
		" Assign Bot PREFIX as environment variable\n Input now for a try>")

MAX_ATTATCHMENTS = 20

bot = Bot(command_prefix = PREFIX)


def make_uuid(length=16):
	""" Join a bunch of characters of the length variable length. """
	return ''.join(sample(alphabet, length))


@bot.event
async def on_ready():
	""" log when bot is online """
	print("Bot is online")


def saving_images(context, uuid_image_dictionary=dict()):
	""" Iterating through attachments and saving them, deleting later. """
	for attachment in context.message.attachments:
		*filename, extension = attachment.filename.split('.')
		filename = '.'.join(filename)
		if not extension in image_types:
			continue
		uuid_image_dictionary[filename] = f"{make_uuid()}.{extension}"
		await attachment.save(
			f"temporary-images/{uuid_image_dictionary[filename]}")
	return uuid_image_dictionary


def who_in_images(context, uuid_image_dictionary):
	for filename in uuid_image_dictionary:
		name = lookup(f"temporary-images/{uuid_image_dictionary[filename]}")
		if name:
			await context.reply("No faces in image.")
		elif name == ">1":
			await context.reply("More than 1 face in image.")
		else:
			await context.reply(
				f"The picture you sent (apparently) looks like {name}",
				file=File(f"faces/{name}.jpg"))
		remove(f"temporary-images/{uuid_image_dictionary[filename]}")


def check_attatchments(context):
	if 0 > len(context.message.attachments):
		return "Attatchments missing"
	elif len(context.message.attachments) > MAX_ATTATCHMENTS:
		return f"Too Many Attatchments!  Please send less than {MAX_ATTATCHMENTS}"
	else:
		return False


@bot.command()
async def main(context):
	if un_safe := check_attatchments(context):
		return await context.reply(un_safe)
	uuid_image_dictionary = saving_images(context)
	who_in_images(context, uuid_image_dictionary)


if __name__ == "__main__":
	bot.run(DISCORD_TOKEN)
