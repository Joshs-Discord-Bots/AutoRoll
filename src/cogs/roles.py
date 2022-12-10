import nextcord
from nextcord.ext import commands

# ------------------------------------------ Custom Classes ------------------------------------------

class CustomRoles():
    def __init__(self, client):
        self.client = client
        self.roles = client.read('./cogs/roles.json')
        if self.roles == None: self.roles = {'games': {}, 'colours': {}}
        return
    
    # If role is a custom role
    def valid(self, role: nextcord.Role):
        for cat in self.roles:
            if str(role.id) in self.roles[cat]:
                return True
        return False
    
    # Write role data to disk
    def save(self):
        self.client.write(self.roles, './cogs/roles.json')
        return

# ------------------------------------------ Drop-downs ------------------------------------------

# Add Games Dropdown
class GameDropdownAdd(nextcord.ui.Select):
    def __init__(self, options):
        if len(options) > 0:
            super().__init__(placeholder='Select a Game(s)', min_values=0, max_values=len(options), options=options)
        else:
            options = [nextcord.SelectOption(label='No availible games!', description='Click to add')]
            super().__init__(placeholder='No availible games!', options=options, disabled=True)
        return
    async def callback(self, interaction: nextcord.Interaction):
        for value in self.values:
            await interaction.user.add_roles(interaction.guild.get_role(int(value)))
            await interaction.response.send_message('Role(s) have been given to you.\nUse `/roles remove` to remove it.**Do NOT reuse dropdown**', ephemeral=True)
        return

# Remove Games Dropdown
class GameDropdownRemove(nextcord.ui.Select):
    def __init__(self, options):
        if len(options) > 0:
            super().__init__(placeholder='Select a Game(s)', min_values=0, max_values=len(options), options=options)
        else:
            options = [nextcord.SelectOption(label='No availible games!', description='Click to add')]
            super().__init__(placeholder='No availible games!', options=options, disabled=True)
        return
    async def callback(self, interaction: nextcord.Interaction):
        for value in self.values:
            await interaction.user.remove_roles(interaction.guild.get_role(int(value)))
            await interaction.response.send_message('Role(s) have been given to you.\nUse `/roles add` to add it.\n**Do NOT reuse dropdown**', ephemeral=True)
        return

# Add Colours Dropdown
class ColourDropdownAdd(nextcord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder='Select a Colour', min_values=0, max_values=1, options=options)
        return
    async def callback(self, interaction: nextcord.Interaction):
        customRoles = CustomRoles(interaction.client)
        # loop through their roles and remove any existing colour roles
        for user_role in interaction.user.roles:
            if str(user_role.id) in customRoles.roles['colours']: 
                await interaction.user.remove_roles(user_role)
        await interaction.user.add_roles(interaction.guild.get_role(int(self.values[0])))
        await interaction.response.send_message('Role has been given to you.\nUse `/roles remove` to remove it.', ephemeral=True)
        return

# Asign to view
class DropdownViewsAdd(nextcord.ui.View):
    def __init__(self, gameOptions, colourOptions):
        super().__init__()
        self.add_item(GameDropdownAdd(gameOptions))
        self.add_item(ColourDropdownAdd(colourOptions))
        return

class DropdownViewsRemove(nextcord.ui.View):
    def __init__(self, gameOptions):
        super().__init__()
        self.add_item(GameDropdownRemove(gameOptions))
        return

# ########################################## Bot ##########################################

class AutoRole(commands.Cog):
    def __init__(self, client):
        self.client = client
        return
    def admin(self, member):
        return True if member.id in self.client.admins else False


# ------------------------------------------ User Commands ------------------------------------------

    @nextcord.slash_command(description='Add/Remove roles')
    async def roles(self, interaction: nextcord.Interaction):
        return
    
    # Add Roles
    @roles.subcommand(description='Give yourself a role')
    async def add(self, interaction: nextcord.Interaction):
        
        # await interaction.response.defer()
        customRoles = CustomRoles(self.client)
        
        gameOptions = []
        colourOptions = []

        for gameID in customRoles.roles['games']:
            gameRole = interaction.guild.get_role(int(gameID))
            if gameRole not in interaction.user.roles:
                gameOptions.append(nextcord.SelectOption(label=gameRole.name, description='Click to add', value=gameID, emoji=customRoles.roles['games'][gameID]))


        for colourID in customRoles.roles['colours']:
            colourOptions.append(nextcord.SelectOption(label=interaction.guild.get_role(int(colourID)).name, description='Click to add', value=colourID, emoji=customRoles.roles['colours'][colourID]))
        
        dropdowns = DropdownViewsAdd(gameOptions, colourOptions)
        embed = nextcord.Embed(title='Server Roles', description='Pick a role(s) you want add and it will be applied to you!', colour=nextcord.Colour.blue())
        await interaction.send(embed=embed, view=dropdowns, ephemeral=True)
        return
        
        

    # Remove Roles
    @roles.subcommand(description='Remove roles')
    async def remove(self, interaction: nextcord.Interaction):
        
        # await interaction.response.defer()
        customRoles = CustomRoles(self.client)
        
        gameOptions = []

        for gameID in customRoles.roles['games']:
            gameRole = interaction.guild.get_role(int(gameID))
            if gameRole in interaction.user.roles:
                gameOptions.append(nextcord.SelectOption(label=gameRole.name, description='Click to remove', value=gameID, emoji=customRoles.roles['games'][gameID]))

        dropdowns = DropdownViewsRemove(gameOptions)
        embed = nextcord.Embed(title='Server Roles', description='Pick a role(s) you want removed and it will be taken from you!', colour=nextcord.Colour.blue())
        await interaction.send(embed=embed, view=dropdowns, ephemeral=True)
        return
    

    @roles.subcommand(description='List available roles')
    async def list(self, interaction: nextcord.Interaction):
        roles = CustomRoles(self.client)
        roleDict = roles.roles
        is_content = False
        
        embed = nextcord.Embed(title='Roles', colour=nextcord.Colour.blue())
        for cat in roleDict:
            if roleDict[cat] == {}: continue
            is_content = True
            roleNames = ''
            for roleID in roleDict[cat]:
                roleNames+=f'{roleDict[cat][roleID]}\t**{interaction.guild.get_role(int(roleID)).name}**\n'
            embed.add_field(name=f'{cat[:-1].capitalize()} Roles', value=roleNames, inline=True)
        
        if not is_content:
            from cogs.megamind import generate
            generate('roles')
            await interaction.send("", files=[nextcord.File('cogs/resources/meme.jpg')])
        else:
            await interaction.send(embed=embed)
        return


# ------------------------------------------ Admin Commands ------------------------------------------
    # Create Role
    @roles.subcommand(description='ADMIN: Add roles to the roster')
    async def create(self, interaction: nextcord.Interaction,
    type: str = nextcord.SlashOption(name='type', choices={'Game': 'games', 'Colour': 'colours'}),
    role: nextcord.Role = nextcord.SlashOption(required=True),
    emoji: str = nextcord.SlashOption(required=True),
    ):
        if not self.admin(interaction.user):
            await interaction.send('You do not have permission to use this command!')
            return

        custRoles = CustomRoles(self.client)
        custRoles.roles[type][str(role.id)] = emoji
        await interaction.send('Role Created!')
        custRoles.save()
        return
    
    
    # Destroy Role
    @roles.subcommand(description='ADMIN: Add roles to the roster')
    async def destroy(self, interaction: nextcord.Interaction,
    type: str = nextcord.SlashOption(name='type', choices={'Game': 'games', 'Colour': 'colours'}),
    role: nextcord.Role = nextcord.SlashOption(required=True),
    ):
        if not self.admin(interaction.user):
            await interaction.send('You do not have permission to use this command!')
            return
        
        custRoles = CustomRoles(self.client)
        if custRoles.valid(role):
            del custRoles.roles[type][str(role.id)]
            await interaction.send('Role Deleted!')
        else:
            await interaction.send('That role does not exist!')
        
        custRoles.save()
        return
    

def setup(client):
    client.add_cog(AutoRole(client))
    return