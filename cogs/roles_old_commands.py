import nextcord
from nextcord.ext import commands
from roles import CustomRoles

# ------------------------------------------ Boilerplate ------------------------------------------

class AutoRole(commands.Cog):
    def __init__(self, client):
        self.client = client
    def admin(self, member):
        return True if member.id in self.client.admins else False

    @nextcord.slash_command(description='Add/Remove roles')
    async def roles(self, interaction: nextcord.Interaction):
        return

# ------------------------------------------ Commands ------------------------------------------

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