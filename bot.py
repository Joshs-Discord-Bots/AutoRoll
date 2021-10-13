#region ------------------------------------------------------ SETUP -------------------------------------------------

from os import system
import discord
from discord.ext import commands
import os
import platform
import json

def read(readFilename):
	try:
		with open(readFilename) as json_file:
			return json.load(json_file)
	except FileNotFoundError:
		return None

def write(data, writeFilename):
	with open(writeFilename, 'w') as outfile:
		json.dump(data, outfile, indent=4)
	return

if not os.path.isfile('config.json'):
	def_config = {
		'token': 'TOKEN',
		'name': 'BOT NAME',
		'intents': {'messages': False, 'members': False, 'guilds': False},
		'prefix': '-',
		'admins': []
	}
	write(def_config, 'config.json')

config = read('config.json')

intents = discord.Intents.default()
intents.messages = config['intents']['messages']
intents.members = config['intents']['members']
intents.guilds = config['intents']['guilds']

prefix = config['prefix']

activity = discord.Game(name=f"{prefix}help")
bot = commands.Bot(command_prefix = prefix, intents=intents, activity=activity, status=discord.Status.online, case_insensitive=True)
bot.remove_command('help')

bot.token = config['token']
bot.admins = config['admins']


#endregion

#region ------------------------------------------------- CUSTOM FUNCTIONS -------------------------------------------

def clear():
	if platform.system() == 'Windows':
		system('cls')
	else:
		# system('clear')
		pass

def admin(ctx):
	return True if ctx.author.id in bot.admins else False
#endregion

#region ----------------------------------------------------- EVENTS -------------------------------------------------

@bot.event																	# Startup
async def on_ready():
	clear()
	print(f'{bot.user} has connected to Discord!')
	me = bot.get_user(285311305253126145)
	await me.send(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
	print('"' + member.name + '" joined')
	if not member.bot:
		role = discord.utils.get(member.guild.roles, name='Silenced')
		await member.add_roles(role) # Silence
		print('"' + member.name + '" has been silenced')
	else:
		role = discord.utils.get(member.guild.roles, name='BOTS')
		await member.add_roles(role) # BOTS
		print('"' + member.name + '" has been given the BOTS role')

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
async def test(ctx):
	if admin(ctx):
		await ctx.author.send('Test')

@bot.command()
async def support(ctx):
	embed = discord.Embed ( # Message
		title='Bot Support Contact Info',
		description='Hey! Problem with the bot? Want your own bot commissioned?\nSend me a friend request!\nJoshalot#1023',
		colour=discord.Colour.orange()
	)
	await ctx.author.send(embed=embed)

@bot.command()
async def reload(ctx):
	if admin(ctx):
		await ctx.send('Reloading...')
		if platform.system() == 'Windows' and os.path.isfile('run.bat'):
			os.system('run.bat')
			quit()
		elif os.path.isfile('run.sh'):
			os.system('./run.sh')
			quit()
		else:
			await ctx.send('An error has occured')
	else:
		await ctx.send('You do not have permission to do that!')

@bot.command()
async def help(ctx):
	await support(ctx)
	return
	embed = discord.Embed ( # Message
		title='Help Commands',
		description=f'Listing commands...',
		colour=discord.Colour.blue()
	)
	# embed.add_field(name=f'{prefix}die', value="die", inline=False)
	await ctx.send(embed=embed)

#endregion

#region ----------------------------------------------------- COGS -------------------------------------------------
blacklist = ['template.py', 'funny_score.py', 'music.py', 'translate.py']

for filename in os.listdir('./cogs'):
	if filename.endswith('.py') and filename not in blacklist:
		bot.load_extension(f'cogs.{filename[:-3]}')

#endregion


clear()
print('Booting Up...')

bot.run(bot.token)