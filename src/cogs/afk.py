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
        return
        
    def save(self):
        self.client.write(self.afkList, './cogs/afk.json')
        return
    
    afkID = 1042296356578017341

    async def setAfk(self, user: nextcord.Member, ctx, method=None):
        '''Usage: <user> <ctx> <give/take/none>'''
        if not method: method = ['give', 'take']
        if type(method) == 'str': method = [method]

        if 'give' in method:
            if str(user.id) not in self.afkList:
                await user.add_roles(ctx.guild.get_role(int(self.afkID)))
                self.afkList[str(user.id)] = int(datetime.now().timestamp())
                self.save()
                await ctx.send(f"**{user.name}** is now AFK.", ephemeral=True)
        elif 'take' in method:
            if str(user.id) in self.afkList:
                await user.remove_roles(ctx.guild.get_role(int(self.afkID)))
                await ctx.guild.rules_channel.send(f'Welcome back **{user.name}**! I have removed your AFK status!')
                self.afkList.pop(str(user.id))
                self.save()
        return
    
    
    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        await self.setAfk(message.author, message, 'take')
        return
    
    @commands.Cog.listener()
    async def on_typing(self, message: nextcord.Message, user: nextcord.Member, when: datetime):
        await self.setAfk(user, message, 'take')
        return
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState):
        await self.setAfk(member, member, 'take')
        return


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
        
        await self.setAfk(interaction.user, interaction)
        return

        

def setup(client):
    client.add_cog(Afk(client))
    return