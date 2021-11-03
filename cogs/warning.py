import discord
from discord.ext import commands
from discord.ext import tasks
import json
from datetime import datetime
from os import system

class Warning(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		self.warningFile = 'warnings.json'
		self.silenceTimes = {
			3: 30,
			4: 60,
			5: 120
		}
		self.checkTime.start()
	
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
		if oldServers == None:
			return None
		newServers = {}
		for oldKey in oldServers:
			if isinstance(oldKey, str):
				newKey = int(oldKey)
				newServers[newKey] = oldServers[oldKey]
			else:
				newServers[oldKey] = oldServers[oldKey]
		return newServers

	def calcTime(self, minutes):
		now = datetime.now()
		hours = 0
		days = 0
		while now.minute+minutes > 59:
			hours+=1
			minutes = minutes-60
		while now.hour+hours > 23:
			days+=1
			hours = hours -24
		then = now.replace(day=now.day+days, hour=now.hour+hours, minute=now.minute+minutes)
		return then

	@tasks.loop(seconds=5)
	async def checkTime(self):
		# print('check')
		warnings = self.dicKeyToInt(self.read(self.warningFile))
		if warnings == None:
			return
		
		for guildID in warnings:
			for userID in warnings[guildID]:
				then = warnings[guildID][userID]['time']
				if then != 0:
					then = datetime.fromisoformat(then)
					if datetime.now() > then:
						warnings[guildID][userID]['time'] = 0
						self.write(warnings, self.warningFile)
						guild = await self.bot.fetch_guild(guildID)
						user = await guild.fetch_member(userID)
						role = discord.utils.get(guild.roles, name='Silenced')
						await user.remove_roles(role)


	@commands.command()
	async def warn(self, ctx, user: discord.Member = None, reason = 'No reason given'):
		if not self.admin(ctx.author):
			await ctx.send('You do not have permission to do that!')
			return
		if user.bot:
			await ctx.send('Please enter/ping a valid user!')
			return
		
		warnings = self.dicKeyToInt(self.read(self.warningFile))

		if warnings == None:
			warnings = {}
		else:
			for server in warnings: 
				warnings[server] = self.dicKeyToInt(warnings[server])
		if ctx.guild.id not in warnings:
			warnings[ctx.guild.id] = {}
		if user.id not in warnings[ctx.guild.id]:
			warnings[ctx.guild.id][user.id] = {'warnings': [], 'time': 0}
		warnings[ctx.guild.id][user.id]['warnings'].append(reason)

		self.write(warnings, self.warningFile)
		await ctx.send(f'`{user.name}` has received a warning!')
		
		usersWarnings = warnings[ctx.guild.id][user.id]['warnings']
		times = list(self.silenceTimes.keys())
		warningNum = len(usersWarnings)
		role = discord.utils.get(user.guild.roles, name='Silenced')
		for time in times:
			if time == warningNum:
				warnings[ctx.guild.id][user.id]['time'] = str(self.calcTime(self.silenceTimes[time]))
				await user.add_roles(role) # Silence
				await ctx.send(f'This user has been silenced for `{self.silenceTimes[time]}` minutes!')
				await user.send(f'*You have been silenced.*\n*Reason:* {usersWarnings[-1]}')
				break
			elif warningNum >= times[-1]:
				warnings[ctx.guild.id][user.id]['time'] = str(self.calcTime(self.silenceTimes[times[-1]]))
				await user.add_roles(role) # Silence
				await ctx.send(f'This user has been silenced for `{self.silenceTimes[times[-1]]}` minutes!')
				await user.send(f'*You have been silenced.*\n*Reason:* {usersWarnings[-1]}')
				break
		self.write(warnings, self.warningFile)

	@commands.command()
	async def warnings(self, ctx, user: discord.Member = None):
		self.warningFile = 'warnings.json'
		if user == None:
			user = ctx.author
		
		embed = discord.Embed ( # Message
		title=f'Warning List: {user.name}',
		colour=discord.Colour.red()
		)
		
		warnings = self.dicKeyToInt(self.read(self.warningFile))
		for server in warnings: 
			warnings[server] = self.dicKeyToInt(warnings[server])

		if warnings == None or ctx.guild.id not in warnings or not warnings[ctx.guild.id]:
			embed.description = 'There are no users with warnings!'
		elif user.id not in warnings[ctx.guild.id] or len(warnings[ctx.guild.id][user.id]['warnings']) == 0:
			embed.description = 'This user has no warnings!'
		else:
			list = ''
			for i, warning in enumerate(warnings[ctx.guild.id][user.id]['warnings']):
				list += f'**{i+1}**: {warning}\n'
			embed.description = list
		await ctx.send(embed=embed)
	

	@commands.command()
	async def warnRemove(self, ctx, user: discord.Member = None, num = None):
		
		self.warningFile = 'warnings.json'

		if not self.admin(ctx.author):
			await ctx.send('You do not have permission to do that!')
			return
		if user == None:
			await ctx.send('Please enter/ping a valid user!')
			return
		if num == None or (num != 'all' and not num.isnumeric()) or (num.isnumeric() and int(num) <= 0):
			await ctx.send('Please enter a valid number!')
			return

		warnings = self.dicKeyToInt(self.read(self.warningFile))
		for server in warnings: 
			warnings[server] = self.dicKeyToInt(warnings[server])

		if warnings == None or ctx.guild.id not in warnings or user.id not in warnings[ctx.guild.id]:
			await ctx.send('This user has no warnings!')
			return

		userWarnings = warnings[ctx.guild.id][user.id]['warnings']
		if num != 'all':
			if int(num) > len(userWarnings):
				await ctx.send(f'This user only has {len(userWarnings)} warnings!')
				return

			warnings[ctx.guild.id][user.id]['warnings'].pop(int(num)-1)
			await ctx.send(f'Warning removed from `{user.name}`')
		else:
			warnings[ctx.guild.id][user.id]['warnings'] = []
			await ctx.send(f'All warnings removed from `{user.name}`')

		self.write(warnings, self.warningFile)

def setup(bot):
	bot.add_cog(Warning(bot))