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
        'intents': {'messages': False, 'members': False, 'guilds': False},
        'prefix': '-',
        'admins': []
    }
    write(def_config, 'config.json')

config = read('config.json')


intents = nextcord.Intents.default()
intents.message_content = config['intents']['messages']
intents.members = config['intents']['members']
intents.guilds = config['intents']['guilds']

prefix = config['prefix']

client = commands.Bot(command_prefix=prefix, intents=intents)
client.token = config['token']
client.admins = config['admins']

#endregion

#region ------------------------------------------------- STARTUP FUNCTIONS -------------------------------------------

def clear():
    if platform.system() == 'Windows':
        system('cls')
    else:
        system('clear')

def admin(member):
    return True if member.id in client.admins else False

@client.event
async def on_ready():
    clear()
    print(f'{client.user} has connected to Discord!')


#endregion
#region ----------------------------------------------------- COGS -------------------------------------------------

whitelist = ['calendar.py']
cogs = [] # So we can reload them
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename in whitelist:
        cog = f'cogs.{filename[:-3]}'
        client.load_extension(cog)
        cogs.append(cog)


#endregion
clear()
print('Booting Up...')

client.run(client.token)