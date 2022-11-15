import nextcord
from nextcord.ext import commands
import matplotlib.pyplot as plt

def generate(big, small, title):
    output='cogs/resources/pie.jpg'
    labels = big, small
    sizes = [95, 5]
    _, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels)
    ax1.set_title(title)
    ax1.axis('equal')
    plt.savefig(output)



class Pie(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(description='Creates a "Pie graph" meme.')
    async def pie(self, interaction: nextcord.Interaction, title: str, big: str, small: str):
        generate(big, small, title)
        await interaction.send("", files=[nextcord.File('cogs/resources/pie.jpg')])

def setup(client):
    client.add_cog(Pie(client))