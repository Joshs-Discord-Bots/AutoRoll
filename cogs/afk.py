import nextcord
from nextcord.ext import commands
import os
from datetime import datetime

class Afk(commands.Cog):
    def __init__(self, client):
        self.client = client
        if os.path.isfile('./cogs/afk.json'):
            self.afkList = client.read('./cogs/afk.json')
        else:
            self.afkList = {}
        
    def save(self):
        self.client.write(self.afkList, './cogs/afk.json')
    
    afkID = 1042296356578017341

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if str(message.author.id) in self.afkList:
            await message.author.remove_roles(message.guild.get_role(int(self.afkID)))
            await message.guild.rules_channel.send(f'Welcome back {message.author.mention}! I have removed your AFK status!')
            self.afkList.pop(str(message.author.id))
            self.save()
            
    @nextcord.slash_command(description='Set your status to afk')
    async def afk(self, interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(required=False)
    ):
        if user:
            if str(user.id) in self.afkList:
                await interaction.send(f"**{user.name}** went AFK <t:{self.afkList[str(user.id)]}:R>", ephemeral=True)
            else:
                await interaction.send(f"**{user.name}** is not AFK!", ephemeral=True)
            return

        if str(interaction.user.id) not in self.afkList:
            await interaction.user.add_roles(interaction.guild.get_role(int(self.afkID)))
            self.afkList[str(interaction.user.id)] = int(datetime.now().timestamp())
            self.save()
            await interaction.response.send_message(f"{interaction.user.mention} is now AFK.")
        else:
            await interaction.user.remove_roles(interaction.guild.get_role(int(self.afkID)))
            self.afkList.pop(str(interaction.user.id))
            self.save()
            await interaction.response.send_message('You are no longer AFK', ephemeral=True)
            return

def setup(client):
    client.add_cog(Afk(client))