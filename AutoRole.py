#region ------------------------------------------------------ SETUP -------------------------------------------------

from os import system
import discord
from discord.ext import commands
import os
import yaml

intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.guilds = True

prefix = '.'

#region status
'''
activity = discord.Streaming(name="!help", url="twitch_url_here")
activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
'''
#endregion

#activity = discord.Game(name=f"{prefix}help")
activity = discord.Game(name='Autorole')
bot = commands.Bot(command_prefix = prefix, intents=intents, activity=activity, status=discord.Status.idle, case_insensitive=True)
bot.remove_command("help")

bot.token = 'TOKEN'
with open('token.txt') as f:
    bot.token = f.read()

bot.id = 863597402270072834
bot.admins = [
	285311305253126145 # Josh
	]

system('cls')
print('Booting Up...')

#endregion

#region ------------------------------------------------- CUSTOM FUNCTIONS -------------------------------------------

clear = lambda: system('cls') #on Windows System

def read(readFilename):
	try:
		with open(readFilename) as f:
			return yaml.load(f, Loader=yaml.FullLoader)
	except FileNotFoundError:
		return None

def write(data, writeFilename):
	with open(writeFilename, 'w') as f:
		data = yaml.dump(data, f)
	return

def admin(ctx):
	admins = [
		285311305253126145 # Josh
		]
	return True if ctx.author.id in admins else False

config = read('config.yaml')

#endregion

#region ----------------------------------------------------- EVENTS -------------------------------------------------

@bot.event																	# Startup
async def on_ready():
	clear()
	print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
	print('"' + member.name + '" joined')
	if not member.bot:
		role = discord.utils.get(member.guild.roles, name='Silenced')
		await member.add_roles(role) # Silence
		print('"' + member.name + '" has been silenced')

@bot.event
async def on_raw_message_edit(payload):
	pass

#endregion

#region ----------------------------------------------------- COMMANDS -------------------------------------------------

@bot.command()
async def edit(ctx, channelID, messageID):									# edit command
	if admin(ctx): # if posted by me
		commandMessage = await ctx.channel.fetch_message(ctx.channel.last_message_id)
		await commandMessage.delete()
		
		embed = discord.Embed (
			title='Game Roles',
			description='React to the games you want to be notified about!',
			colour=discord.Colour.blue()
		)
		embed.add_field(name="Role Options:", value="• Minecraft\n• Warframe\n• Dark Souls\n• Stellaris\n• CSGO\n• Among Us\n• TF2\n• Sea of Thieves\n• Factorio\n• GTA", inline=False)
		embed.add_field(name="Role Type", value="Not Unique", inline=False)
		channel = bot.get_channel(int(channelID))
		message = await channel.fetch_message(messageID)
		await message.edit(embed=embed)

@bot.command()
async def botreact(ctx, type, channelID, messageID, reaction):					# react command
	if admin(ctx): # if posted by me
		commandMessage = await ctx.channel.fetch_message(ctx.channel.last_message_id)
		await commandMessage.delete()
		
		channel = bot.get_channel(int(channelID))
		message = await channel.fetch_message(messageID)

		emoji = bot.get_emoji(int(reaction))
		if type == 'remove':
			await message.remove_reaction(emoji, message.author)
		else:
			await message.add_reaction(emoji)

@bot.command()
async def ping(ctx):
	await ctx.send('Pong!')

@bot.command()
async def help(ctx):
	pass
	embed = discord.Embed ( # Message
		title='Help Commands',
		description=f'Listing commands...',
		colour=discord.Colour.blue()
	)
	embed.add_field(name=f'{prefix}autoreact', value="Toggles the upvote/downvote reacts by the bot", inline=False)
	embed.add_field(name=f'{prefix}funnyScore <user>', value="Returns stats on the user's memes", inline=False)
	embed.add_field(name=f'{prefix}leaderboard', value="Displays the top 5 funniest members on the server", inline=False)
	embed.add_field(name=f'{prefix}xp', value="Displays user's xp", inline=False)
	embed.add_field(name=f'{prefix}die', value="die", inline=False)
	embed.add_field(name=f'--- XP ---', value="Users gain XP by posting memes or recieving upvotes.\nUpvoting/Downvoting costs 1 XP.", inline=False)
	msg = await ctx.send(embed=embed)


@bot.command()
async def reload(ctx):
	if admin(ctx):
		await ctx.send('Reloading...')
		os.system('run.bat')
		quit()
	else:
		await ctx.send('You do not have permission to do that!')




#endregion

#region ----------------------------------------------------- COGS -------------------------------------------------
blacklist = ['music.py', 'translate.py']

for filename in os.listdir('./cogs'):
	if filename.endswith('.py') and filename not in blacklist:
		bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(bot.token)