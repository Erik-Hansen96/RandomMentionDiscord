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
user_cache = {}

@bot.event
async def on_ready():
	print('logged in')

@bot.command()
async def someone(ctx):
	server_id = ctx.guild.id
	if server_id not in user_cache:
		user_mentions = []
		for user in ctx.guild.members:
			if not user.bot:
				user_mentions.append(user.mention)
		user_cache[server_id] = user_mentions
	rando = random.choice(user_cache[server_id])
	await ctx.send(rando)

@bot.event
async def on_member_join(member):
	if member.guild.id in user_cache:
		user_cache[member.guild.id].append(member.mention)

@bot.event
async def on_member_remove(member):
	if member.guild.id in user_cache:
		user_cache[member.guild.id].remove(member.mention)

@bot.event
async def on_guild_remove(guild):
	if guild.id in user_cache:
		del user_cache[guild.id]

bot.run(TOKEN)
