#region ------------------------------------------------------ SETUP -------------------------------------------------

import nextcord, os, platform, json, psutil, asyncio, time
from nextcord.interactions import Interaction
from nextcord.ext import commands, application_checks

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

def admin(member):
    return member.id in client.admins

# Create config file
config = {}
envTypes = {
    "str": ['TOKEN', 'DEVTOKEN', 'PREFIX', 'ADMINS'],
    "bool": ['DEVMODE', 'MESSAGES', 'MEMBERS', 'GUILDS', 'VOICE_STATES']
}
# Ensure .env format
for envType in envTypes:
    for envVar in envTypes[envType]:
        envVal = os.environ[envVar]
        # Convert bool string to bools
        if envType == 'bool':
            envVal = os.environ[envVar].lower() in ['true']
        # Check for missing environment variables
        if envVar not in os.environ:
            print(f'"{envVar}" environment variable not initialised! Please ensure you have a VALID .env file')
            print('Please read the README.md file for more details.')
            exit()
        config[envVar] = envVal

intents = nextcord.Intents.default()
intents.message_content = config['MESSAGES']
intents.members = config['MEMBERS']
intents.guilds = config['GUILDS']
intents.voice_states = config['VOICE_STATES']

client = commands.Bot(command_prefix=config['PREFIX'], intents=intents)

client.read = read
client.write = write
client.admin = admin
client.token = config['TOKEN']
client.admins = [int(id) for id in config['ADMINS'].replace(' ','').split(',')]
client.dev = config['DEVMODE']

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

@client.event
async def on_application_command_error(interaction, exception):
    if isinstance(exception, nextcord.ApplicationCheckFailure):
        await interaction.send('check failiure')
    else:
        await interaction.send(exception, ephemeral=True)
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

whitelist = ['misc.py', 'roles.py', 'stats.py', 'afk.py']
cogs = [] # So we can reload them
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename in whitelist:
        cog = f'cogs.{filename[:-3]}'
        client.load_extension(cog)
        cogs.append(cog)

#endregion

print('-'*50)
print('Booting Up...')

while True:
    try:
        if config['DEVMODE']:
            client.run(config['DEVTOKEN'])
        else:
            client.run(config['TOKEN'])
    except:
        print('Failed to start bot')
        print('Retrying in 5 seconds...')
        time.sleep(10)
