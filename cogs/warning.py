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
	
	silenceTimes = {
		3: 30,
		4: 60,
		5: 120
	}
	

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
		for server in warnings: 
			warnings[server] = self.dicKeyToInt(warnings[server])

		if warnings == None:
			warnings = {}
		if ctx.guild.id not in warnings:
			warnings[ctx.guild.id] = {}
		if user.id not in warnings[ctx.guild.id]:
			warnings[ctx.guild.id][user.id] = []
		warnings[ctx.guild.id][user.id].append(reason)

		self.write(warnings, warningFile)
		await ctx.send(f'`{user.name}` has received a warning!')
		
		usersWarnings = warnings[ctx.guild.id][user.id]
		times = list(self.silenceTimes.keys())
		if len(usersWarnings) in times:
			pass


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
		for server in warnings: 
			warnings[server] = self.dicKeyToInt(warnings[server])

		if warnings == None or ctx.guild.id not in warnings or not warnings[ctx.guild.id]:
			embed.description = 'There are no users with warnings!'
		elif user.id not in warnings[ctx.guild.id] or len(warnings[ctx.guild.id][user.id]) == 0:
			embed.description = 'This user has no warnings!'
		else:
			list = ''
			for i, warning in enumerate(warnings[ctx.guild.id][user.id]):
				list += f'**{i+1}**: {warning}\n'
			embed.description = list
		await ctx.send(embed=embed)
	

	@commands.command()
	async def warnRemove(self, ctx, user: discord.Member = None, num = None):
		
		warningFile = 'warnings.json'

		if not self.admin(ctx.author):
			await ctx.send('You do not have permission to do that!')
			return
		if user == None:
			await ctx.send('Please enter/ping a valid user!')
			return
		if num == None or (num != 'all' and not num.isnumeric()) or (num.isnumeric() and int(num) <= 0):
			await ctx.send('Please enter a valid number!')
			return

		warnings = self.dicKeyToInt(self.read(warningFile))
		for server in warnings: 
			warnings[server] = self.dicKeyToInt(warnings[server])

		if warnings == None or ctx.guild.id not in warnings or user.id not in warnings[ctx.guild.id]:
			await ctx.send('This user has no warnings!')
			return

		userWarnings = warnings[ctx.guild.id][user.id]
		if num != 'all':
			if int(num) > len(userWarnings):
				await ctx.send(f'This user only has {len(userWarnings)} warnings!')
				return

			warnings[ctx.guild.id][user.id].pop(int(num)-1)
			await ctx.send(f'Warning removed from `{user.name}`')
		else:
			warnings[ctx.guild.id][user.id] = []
			await ctx.send(f'All warnings removed from `{user.name}`')

		self.write(warnings, warningFile)

	@warnRemove.error
	async def warnRemove_error(self, ctx, error):
		if isinstance(error, commands.MemberNotFound):
			await ctx.send('Please input a valid user!')
	
def setup(bot):
	bot.add_cog(Warning(bot))