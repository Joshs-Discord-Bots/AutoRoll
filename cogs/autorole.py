import nextcord
from nextcord.ext import commands
from typing import Optional

class CustomRoles():
    def __init__(self, client):
        self.client = client
        self.roles = client.read('./cogs/roles.json')
        if self.roles == None: self.roles = {'games': {}, 'colours': {}}
    
    # If role is a custom role
    def valid(self, role: nextcord.Role):
        for cat in self.roles:
            if str(role.id) in self.roles[cat]:
                return True
        return False
    
    # Write role data to disk
    def save(self):
        self.client.write(self.roles, './cogs/roles.json')



class AutoRole(commands.Cog):
    def __init__(self, client):
        self.client = client
    def admin(self, member):
        return True if member.id in self.client.admins else False


    @nextcord.slash_command(description='Add/Remove roles')
    async def roles(self, interaction: nextcord.Interaction):
        return
    
    # Add Roles
    @roles.subcommand(description='Give yourself a role')
    async def add(self, interaction: nextcord.Interaction,
    role: nextcord.Role = nextcord.SlashOption(required=True)):
        custRoles = CustomRoles(self.client)
        if custRoles.valid(role):
            # if the user picked a colour role
            if str(role.id) in custRoles.roles['colours']:
                # loop through their roles and remove any existing colour roles
                for user_role in interaction.user.roles:
                    if str(user_role.id) in custRoles.roles['colours']: 
                        await interaction.user.remove_roles(user_role)

            await interaction.user.add_roles(role)
            await interaction.send(f'**{role.name}** has been given to you.\nUse `/roles remove` to remove it.')
        else:
            await interaction.send('That role is NOT a valid role!\nUser `/roles list` for a list of valid roles.')
        return


    # Remove Roles
    @roles.subcommand(description='Add roles to the roster')
    async def remove(self, interaction: nextcord.Interaction,
    role: nextcord.Role = nextcord.SlashOption(required=True)):
        custRoles = CustomRoles(self.client)
        if custRoles.valid(role):
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.send(f'**{role.name}** has been taken from you.')
            else:
                await interaction.send(f'You do not have that role!')
        else:
            await interaction.send('That role is NOT a valid role!\nUser `/roles list` for a list of valid roles.')
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


    # Admin Commands
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
        custRoles.roles[type][str(role.id)] = {'name': role.name, 'emoji': emoji}
        await interaction.send('Role Created!')
        custRoles.save()
        return
    
    
    # Remove Role
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
    

    # Remove Role
    @roles.subcommand(description='Add roles to the roster')
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

# add subcommands
# https://docs.nextcord.dev/en/stable/interactions.html#:~:text=Slash%20options%20are%20used%20to,additional%20information%20for%20the%20command.&text=The%20option%20can%20be%20type,to%20make%20the%20argument%20optional.