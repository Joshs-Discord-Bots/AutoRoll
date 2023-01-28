#region ------------------------------------------------------ SETUP -------------------------------------------------

import nextcord, os, platform, json, psutil, asyncio, time
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
        "devtoken": os.environ['DEVTOKEN'],
        "intents": {
            "messages": True if 'MESSAGES' in os.environ['INTENTS'] else False,
            "members": True if 'MEMBERS' in os.environ['INTENTS'] else False,
            "guilds": True if 'GUILDS' in os.environ['INTENTS'] else False,
            "voice_states": True if 'VOICE_STATES' in os.environ['INTENTS'] else False,
        },
        "prefix": "$",
        "admins": [int(dcid) for dcid in os.environ['ADMINS'].split(' ')]
    }
else:
    if not os.path.isfile('config.json'):
        def_config = {
            'token': 'TOKEN',
            'devtoken': 'DEVTOKEN',
            'mode': 'NORMAL',
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

client = commands.Bot(command_prefix=config['prefix'], intents=intents)

client.read = read
client.write = write
client.token = config['token']
client.admins = config['admins']


#endregion

#region ------------------------------------------------- CUSTOM FUNCTIONS -------------------------------------------

def admin(member):
    return True if member.id in client.admins else False

#endregion

#region ----------------------------------------------------- EVENTS -------------------------------------------------

@client.event																	# Startup
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name = 'Slash Commands!'))
    return

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
    return

#endregion

#region ----------------------------------------------------- RELOAD COGS -------------------------------------------------

@client.slash_command()
@commands.is_owner()
async def reload_cogs(interaction : nextcord.Interaction):
    if not admin(interaction.user):
        await interaction.send('You do not have permission to use this command!')
        return
    
    for cog in cogs:
        client.reload_extension(cog)
    await interaction.send('Cogs have been reloaded!')
    return

#endregion

#region ----------------------------------------------------- COGS -------------------------------------------------

whitelist = ["stats.py"]
# whitelist = ['test.py', 'roles.py']
cogs = [] # So we can reload them
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename in whitelist:
        cog = f'cogs.{filename[:-3]}'
        client.load_extension(cog)
        cogs.append(cog)

#endregion

print('\n'*5, '-'*50)
print('Booting Up...')

while True:
    try:
        if 'DEV' in os.environ and 'DEVTOKEN' in os.environ:
            client.run(os.environ['DEVTOKEN'])
        else:
            client.run(client.token)
    except:
        print('Failed to start bot')
        print('Retrying in 5 seconds...')
        time.sleep(5)
