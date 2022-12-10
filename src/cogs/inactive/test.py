import nextcord
from nextcord.ext import commands

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client
        return

    @nextcord.slash_command(name='test')
    async def test(self, interaction: nextcord.Interaction ,
    role: nextcord.Role):
        await interaction.send(role.name)
        await interaction.user.remove_roles(role)
        return

def setup(client):
    client.add_cog(Test(client))
    return