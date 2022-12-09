#region ------------------------------------------------------ SETUP -------------------------------------------------

import nextcord, os, platform, json, psutil, asyncio
from time import sleep
from nextcord.ext import commands

def read(readFilename, raw=False):
    try:
        with open(readFilename) as file:
            if raw:
                return file.read()
            else:
                return json.load(file)
    except FileNotFoundError:
        print('File not found!')
        return None

def write(data, writeFilename):
    with open(writeFilename, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    return

if 'TOKEN' in os.environ: # If in docker container
    config = {
        "token": os.environ['TOKEN'],
        "intents": {
            "messages": True if 'MESSAGES' in os.environ['INTENTS'] else False,
            "members": True if 'MEMBERS' in os.environ['INTENTS'] else False,
            "guilds": True if 'GUILDS' in os.environ['INTENTS'] else False,
            "voice_states": True if 'VOICE_STATES' in os.environ['INTENTS'] else False,
        },
        "prefix": "$",
        "admins": [285311305253126145]
    }
else:
    if not os.path.isfile('config.json'):
        def_config = {
            'token': 'TOKEN',
            'intents': {'messages': False, 'members': False, 'guilds': False, 'voice_states': False},
            'prefix': '-',
            'admins': []
        }
        write(def_config, 'config.json')

    config = read('config.json')


intents = nextcord.Intents.default()
intents.message_content = config['intents']['messages']
intents.members = config['intents']['members']
intents.guilds = config['intents']['guilds']
intents.voice_states = config['intents']['voice_states']

prefix = config['prefix']

# activity = discord.Game(name=f"{prefix}help")
# bot = commands.Bot(command_prefix = prefix, intents=intents, activity=activity, status=discord.Status.online, case_insensitive=True)
# client.remove_command('help')


# bot = nextcord.Client()
client = commands.Bot(command_prefix=prefix, intents=intents)
client.token = config['token']
client.admins = config['admins']

client.read = read
client.write = write


#endregion

#region ------------------------------------------------- CUSTOM FUNCTIONS -------------------------------------------

def clear():
    return
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def admin(member):
    return True if member.id in client.admins else False

async def checkBattery(client, limit):
    flag = False
    while True:
        battery = psutil.sensors_battery()
        if battery.percent < limit and not flag:
            print('battery is at ', battery.percent)
            flag = True
            pings = ' '.join(str(client.get_user(user).mention) for user in client.admins)
            await client.get_channel(899734389724942396).send(f'{pings} Battery is low! Please charge me!')
        else:
            flag = False
        await asyncio.sleep(300)

#endregion

#region ----------------------------------------------------- EVENTS -------------------------------------------------

@client.event																	# Startup
async def on_ready():
    clear()
    print(f'{client.user} has connected to Discord!')
    await checkBattery(client, 15)

@client.event
async def on_message(message):
    pass
    # print(message.content)

@client.event
async def on_member_join(member):
    print('"' + member.name + '" joined')
    if not member.bot:
        role = member.guild.get_role(870593338468872192)
        await member.add_roles(role) # Silence
        print('"' + member.name + '" has been silenced')
    else:
        role = member.guild.get_role(675635324071706654)
        await member.add_roles(role) # BOTS
        print('"' + member.name + '" has been given the BOTS role')



# @client.event
# async def on_command_error(ctx, error):
# 	if isinstance(error, commands.MemberNotFound):
# 		await ctx.send('That user does not exist!')
# 	elif isinstance(error, commands.MissingPermissions):
# 		await ctx.send('You are not allowed to do that!')

#endregion

#region ----------------------------------------------------- COMMANDS -------------------------------------------------

@client.slash_command(description='Will return "Pong" if the bot is online.')
async def ping(interaction : nextcord.Interaction):
    await interaction.send(f'🏓 **Pong!** ({round(client.latency*1000)}ms)')

@client.slash_command(description='Will return the battery of the bot.', guild_ids=[330974948870848512])
async def battery(interaction : nextcord.Interaction):
    battery = psutil.sensors_battery()
    colour = nextcord.Colour.green() if battery.percent > 15 else nextcord.Colour.red()

    def convertTime(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%d:%02d:%02d" % (hours, minutes, seconds)
    
    embed = nextcord.Embed(title="Server Battery Stats", colour=colour)
    embed.add_field(name='Battery percentage:', value=f'`{round(battery.percent, 2)}%`', inline=False)
    embed.add_field(name='Power plugged in:', value=f'`{battery.power_plugged}`', inline=False)
    embed.add_field(name='Battery time remaining:', value=f'`{convertTime(battery.secsleft)}`', inline=False)
    await interaction.send(embed=embed)
    return

@client.slash_command(description='Help Command')
async def help(interaction : nextcord.Interaction):
    # await support(interaction)
    # return
    
    embed = nextcord.Embed(
        title='Help Commands',
        description=f'Listing commands...',
        colour=nextcord.Colour.blue())
    embed.add_field(name='/ping', value='Will return "Pong" if the bot is online.', inline=False),
    embed.add_field(name='/roles <add/remove/list>', value='Commands relating to roles.', inline=False),
    embed.add_field(name='/no <keyword>', value='Creates a custom "No Bitches?" meme.', inline=False),
    await interaction.send(embed=embed)

@client.slash_command(description='Help Command alias')
async def support(interaction : nextcord.Interaction):
    embed = nextcord.Embed(
        title='Bot Support Contact Info',
        description='Hey! Problem with the bot? Want your own bot commissioned?\nSend me a friend request!\n\n@Joshalot#1023',
        color=nextcord.Color.orange())
    await interaction.send(embed=embed)

@client.slash_command()
@commands.is_owner()
async def reload_cogs(interaction : nextcord.Interaction):
    if not admin(interaction.user):
        await interaction.send('You do not have permission to use this command!')
        return
    
    for cog in cogs:
        client.reload_extension(cog)
    await interaction.send('Cogs have been reloaded!')


@client.slash_command()
@commands.is_owner()
async def reload(interaction : nextcord.Interaction):
    return
    if admin(interaction.user):
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


#endregion

#region ----------------------------------------------------- COGS -------------------------------------------------

whitelist = ['roles.py', 'megamind.py', 'afk.py']
# whitelist = ['test.py', 'roles.py']
cogs = [] # So we can reload them
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename in whitelist:
        cog = f'cogs.{filename[:-3]}'
        client.load_extension(cog)
        cogs.append(cog)

#endregion
clear()
print('\n'*5, '-'*50)
print('Booting Up...')

client.debug = False

while True:
    try:
        if client.debug:
            client.run(read('TEST_AUTH', raw=True))
        else:
            client.run(client.token)
    except:
        print('Failed to start bot')
        print('Retrying in 5 seconds...')
        sleep(5)
