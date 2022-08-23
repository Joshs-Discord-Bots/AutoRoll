#region ------------------------------------------------------ SETUP -------------------------------------------------

from os import system
import nextcord
from nextcord.ext import commands
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
		# 'intents': {'messages': False, 'members': False, 'guilds': False},
		# 'prefix': '-',
		'admins': []
	}
	write(def_config, 'config.json')

config = read('config.json')

# intents = discord.Intents.default()
# intents.messages = config['intents']['messages']
# intents.members = config['intents']['members']
# intents.guilds = config['intents']['guilds']

# prefix = config['prefix']

# activity = discord.Game(name=f"{prefix}help")
# bot = commands.Bot(command_prefix = prefix, intents=intents, activity=activity, status=discord.Status.online, case_insensitive=True)
# bot.remove_command('help')


bot = nextcord.Client()
bot.token = config['token']
bot.admins = config['admins']


#endregion

#region ------------------------------------------------- CUSTOM FUNCTIONS -------------------------------------------

def clear():
	if platform.system() == 'Windows':
		system('cls')
	else:
		system('clear')

def admin(ctx):
	return True if ctx.author.id in bot.admins else False
#endregion

#region ----------------------------------------------------- EVENTS -------------------------------------------------

@bot.event																	# Startup
async def on_ready():
	clear()
	print(f'{bot.user} has connected to Discord!')
	# me = bot.get_user(285311305253126145)
	# await me.send(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
	print('"' + member.name + '" joined')
	# if not member.bot:
	# 	role = discord.utils.get(member.guild.roles, name='Silenced')
	# 	await member.add_roles(role) # Silence
	# 	print('"' + member.name + '" has been silenced')
	# else:
	# 	role = discord.utils.get(member.guild.roles, name='BOTS')
	# 	await member.add_roles(role) # BOTS
	# 	print('"' + member.name + '" has been given the BOTS role')



# @bot.event
# async def on_command_error(ctx, error):
# 	if isinstance(error, commands.MemberNotFound):
# 		await ctx.send('That user does not exist!')
# 	elif isinstance(error, commands.MissingPermissions):
# 		await ctx.send('You are not allowed to do that!')

#endregion

#region ----------------------------------------------------- COMMANDS -------------------------------------------------

# @bot.command()
# async def ping(ctx):
# 	await ctx.send('Pong!')

# @bot.command()
# async def test(ctx):
#     pass

# @bot.command()
# async def support(ctx):
# 	embed = discord.Embed ( # Message
# 		title='Bot Support Contact Info',
# 		description='Hey! Problem with the bot? Want your own bot commissioned?\nSend me a friend request!\n\nJoshalot#1023',
# 		colour=discord.Colour.orange()
# 	)
# 	await ctx.author.send(embed=embed)

@bot.slash_command()
async def reload(interaction : nextcord.Interaction):
	# if admin(ctx):
	if True:
		await interaction.send('Reloading...')
		if platform.system() == 'Windows' and os.path.isfile('run.bat'):
			os.system('run.bat')
			quit()
		elif os.path.isfile('run.sh'):
			os.system('./run.sh')
			quit()
		else:
			await interaction.send('An error has occured')
	else:
		await interaction.send('You do not have permission to do that!')

# @bot.command()
# async def help(ctx):
# 	await support(ctx)
# 	return
# 	embed = discord.Embed ( # Message
# 		title='Help Commands',
# 		description=f'Listing commands...',
# 		colour=discord.Colour.blue()
# 	)
# 	# embed.add_field(name=f'{prefix}die', value="die", inline=False)
# 	await ctx.send(embed=embed)

#endregion

#region ----------------------------------------------------- COGS -------------------------------------------------
# blacklist = ['template.py', 'funny_score.py', 'music.py', 'translate.py']

# for filename in os.listdir('./cogs'):
# 	if filename.endswith('.py') and filename not in blacklist:
# 		bot.load_extension(f'cogs.{filename[:-3]}')

#endregion

clear()
print('Booting Up...')

bot.run(bot.token)