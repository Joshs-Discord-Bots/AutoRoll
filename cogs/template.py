import discord
from discord.ext import commands

class Title(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	
	#@commands.command()

	#@commands.Cog.listener()

def setup(bot):
	bot.add_cog(Title(bot))