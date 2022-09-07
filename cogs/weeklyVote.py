import nextcord
from nextcord.ext import commands

class WeeklyVote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name='test')
    async def test(self, interaction: nextcord.Interaction):
        await interaction.send('test')

def setup(client):
    client.add_cog(WeeklyVote(client))