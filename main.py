###########################################
# WhoRU Discord Bot
# Recognise which celebrity you look like!
###########################################
import recognise_face

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
client = commands.Bot(command_prefix=PREFIX)

@client.event
async def on_ready():
	print("Bot is online")

###########################################
# On Message
###########################################
@client.event
async def on_message(message):
	print(f"{message.author.display_name}: {message.content}")

###########################################
# On Message
###########################################
@client.command()
async def who(ctx):


###########################################
# Inserting token
###########################################
client.run(DISCORD_TOKEN)
