import nextcord
from nextcord.ext import commands

# Create Dropdown
class GameDropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label='Option 1', description='Description', emoji='\ud83d\udfe3'),
            nextcord.SelectOption(label='Option 2', description='Description'),
            nextcord.SelectOption(label='Option 3', description='Description'),
        ]
        super().__init__(placeholder='Select an Option', min_values=0, max_values=len(options), options=options)
    
    async def callback(self, interaction: nextcord.Interaction):
        print(self.values)
        await interaction.response.send_message(f'You chose {self.values[0]}')

# Asign to view
class GameDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GameDropdown())


# Cog command
class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name='test')
    async def test(self, interaction: nextcord.Interaction,
    type: str = nextcord.SlashOption(name='type', choices={'Game': 'games', 'Colour': 'colours'})):
        from cogs.autorole import CustomRoles
        customRoles = CustomRoles
        gameDropdown = GameDropdownView()
        embed = nextcord.Embed(title='Game Roles', description='Pick and game you want and it will be applied as a role!' colour=nextcord.Colour.blue())
        await interaction.send('test', embed=embed, view=gameDropdown)



def setup(client):
    client.add_cog(Test(client))