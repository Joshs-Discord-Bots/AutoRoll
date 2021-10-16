import discord
from discord.ext import commands
import json
import os

class Warning(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	
	def admin(self, user):
		return user.id in self.bot.admins or user.guild_permissions.administrator

	def read(self, readFilename):
		try:
			with open(readFilename) as json_file:
				return json.load(json_file)
		except FileNotFoundError:
			return None

	def write(self, data, writeFilename):
		with open(writeFilename, 'w') as outfile:
			json.dump(data, outfile, indent=4)
		return

	def dicKeyToInt(self, oldServers):
		newServers = {}
		for oldKey in oldServers:
			if isinstance(oldKey, str):
				newKey = int(oldKey)
				newServers[newKey] = oldServers[oldKey]
			else:
				newServers[oldKey] = oldServers[oldKey]
		return newServers
	

	@commands.command()
	async def warn(self, ctx, user: discord.Member = None, reason = 'No reason given'):
		warningFile = 'warnings.json'

		if not self.admin(ctx.author):
			await ctx.send('You do not have permission to do that!')
			return
		if user == None:
			await ctx.send('Please enter/ping a valid user!')
			return
		
		warnings = self.dicKeyToInt(self.read(warningFile))

		if warnings == None:
			warnings = {}
		if ctx.guild.id not in warnings:
			warnings[ctx.guild.id] = {}
		if str(user.id) not in warnings[ctx.guild.id]:
			warnings[ctx.guild.id][user.id] = []
		warnings[ctx.guild.id][user.id].append(reason)

		self.write(warnings, warningFile)
		await ctx.send(f'`{user.name}` has received a warning!')

	@commands.command()
	async def warnings(self, ctx, user: discord.Member = None):
		warningFile = 'warnings.json'
		if user == None:
			await ctx.send('Please enter/ping a valid user!')
			return
		
		embed = discord.Embed ( # Message
		title=f'Warning List: {user.name}',
		colour=discord.Colour.red()
		)
		
		warnings = self.dicKeyToInt(self.read(warningFile))

		if warnings == None or ctx.guild.id not in warnings or not warnings[ctx.guild.id]:
			embed.description = 'There are no users with warnings!'
		elif user.id not in warnings[ctx.guild.id]:
			embed.description = 'This user has no warnings!'
		else:
			for i, warning in enumerate(warnings[ctx.guild.id][user.id]):
				embed.add_field(name=i, value=warning, inline=False)
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Warning(bot))