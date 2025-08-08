import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver
import yt_dlp

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

role_saban = "saban"

@bot.event
async def on_ready():
	print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
	await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	if "kreten" in message.content.lower():
		await message.delete()
		await message.channel.send(f"{message.author.mention}, mojne se glupiras.")

	await bot.process_commands(message)

@bot.command()
async def dm(ctx, *, msg):
	await ctx.author.send(f"You said {msg}")

@bot.command()
@commands.has_role(role_saban)
async def reply(ctx):
	await ctx.reply(f"{ctx.author.mention} tu smo bato, sta treba?")

@reply.error
async def reply_error(ctx, error):
	if isinstance(error, commands.MissingRole):
		await ctx.reply(f"{ctx.author.mention}, sta hoces bre ti?")

@bot.command()
async def hello(ctx):
	await ctx.send(f"Hello {ctx.author.mention}")

@bot.command()
async def assign(ctx):
	role = discord.utils.get(ctx.guild.roles, name=role_saban)
	if role:
		await ctx.author.add_roles(role)
		await ctx.send(f"{ctx.author.mention} is now assigned to {role_saban}")
	else:
		await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
	role = discord.utils.get(ctx.guild.roles, name=role_saban)
	if role:
		await ctx.author.remove_roles(role)
		await ctx.send(f"{ctx.author.mention} has had the {role_saban} removed")
	else:
		await ctx.send("Role doesn't exist")

@bot.command()
@commands.has_role(role_saban)
async def secret(ctx):
	await ctx.send(f"{ctx.author.mention}, welcome to Srbija!")

@secret.error
async def secret_error(ctx, error):
	if isinstance(error, commands.MissingRole):
		await ctx.send(f"{ctx.author.mention}, pa ne moze to tako prijatelju!")

@bot.command()
async def poll(ctx, *, question):
	embed = discord.Embed(title="New Poll", description=question)
	poll_message = await ctx.send(embed=embed)
	await poll_message.add_reaction("👍")
	await poll_message.add_reaction("👎")

@bot.command()
async def play(ctx, *, song):
	if ctx.author.voice is None:
		await ctx.send("🔇 You need to be in a voice channel.")
		return

	user_voice_channel = ctx.author.voice.channel

	if ctx.voice_client is None:
		await user_voice_channel.connect()
	elif ctx.voice_channel.channel != user_voice_channel:
		await ctx.voice_client.move_to(user_voice_channel)

	await ctx.send(f"🔍 Searching for: `{song}`...")

	ydl_opts = {
		'format': 'bestaudio/best',
		'quiet': True,
		'extract_flat': False,
		'noplaylist': True,
		'extract_flat': False,
		'force_generic_extractor': False
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(f"ytsearch:{song}", download=False)['entries'][0]
		url = info['url']
		title = info.get('title', 'Unknown Title')
		webpage_url = info.get('webpage_url')

	vc = ctx.voice_client
	if vc.is_playing():
		vc.stop()

	ffmpeg_opts = {'options': '-vn'}
	vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_opts))

	await ctx.send(f"🎶 Now playing: **{title}**\n🔗 {webpage_url}")

@bot.command()
async def leave(ctx):
	if ctx.voice_client:
		await ctx.voice_client.disconnect()
		await ctx.send("👋 Left the voice channel.")
	else:
		await ctx.send("I'm not in any voice channel.")

#webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)