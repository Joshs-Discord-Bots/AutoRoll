#region ------------------------------------------------------ SETUP -------------------------------------------------

import nextcord, os, platform, json
from nextcord.ext import commands

def read(readFilename):
    try:
        with open(readFilename) as json_file:
            return json.load(json_file)
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
            "messages": True,
            "members": True,
            "guilds": True
        },
        "prefix": "$",
        "admins": [285311305253126145]
    }
else:
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
#endregion

#region ----------------------------------------------------- EVENTS -------------------------------------------------

@client.event																	# Startup
async def on_ready():
    clear()
    print(f'{client.user} has connected to Discord!')

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

whitelist = ['autorole.py', 'megamind.py', 'test.py']
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