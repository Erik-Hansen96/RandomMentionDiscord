import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='@', intents=intents)

@bot.event
async def on_ready():
	print('logged in')

# To avoid excessive API calls and increase speed
server_cache = {}

# Mention random user command
@bot.command()
async def someone(ctx):
	server_id = ctx.guild.id

	# Check if the server is already cached
	if server_id not in server_cache:
		user_mentions = []

		# If not in cache, add all users to a list
		for user in ctx.guild.members:
			if not user.bot:
				user_mentions.append(user.mention)

		server_cache[server_id] = user_mentions # Add list to cache

	rando = random.choice(server_cache[server_id])
	await ctx.send(rando)

# When a user joins a cached server, add them to the cache
@bot.event
async def on_member_join(user):
	if user.guild.id in server_cache:
		server_cache[user.guild.id].append(user.mention)

# When a user leaves a cached server, remove them from cache
@bot.event
async def on_member_remove(user):
	if user.guild.id in server_cache:
		server_cache[user.guild.id].remove(user.mention)

# If a server removes the bot, remove server from cache
@bot.event
async def on_guild_remove(guild):
	if guild.id in server_cache:
		del server_cache[guild.id]

bot.run(TOKEN)
