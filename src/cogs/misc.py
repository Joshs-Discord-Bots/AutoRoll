import nextcord
from nextcord.ext import commands

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
        return

    @nextcord.slash_command(name='Ping', description='Will return "Pong" if the bot is online.')
    async def ping(self, interaction : nextcord.Interaction):
        await interaction.send(f'🏓 **Pong!** ({round(client.latency*1000)}ms)')
        return

    @nextcord.slash_command(name='Help', description='Help Command alias')
    async def support(self, interaction : nextcord.Interaction):
        embed = nextcord.Embed(
            title='Bot Support Contact Info',
            description='Hey! Problem with the bot? Want your own bot commissioned?\nSend me a friend request!\n\n@Joshalot#1023',
            color=nextcord.Color.orange())
        await interaction.send(embed=embed)
        return



def setup(client):
    client.add_cog(Misc(client))
    return
