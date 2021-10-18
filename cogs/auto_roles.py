import discord
from discord.ext import commands

class AutoRole(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot

	#region ---------------------------------------------------- FUNCTIONS -----------------------------------------------

	def admin(self, ctx):
		return True if ctx.author.id in self.admins else False

	def getGuild(self, ctx):
		guild = discord.utils.find(lambda g : g.id == ctx.guild_id, self.bot.guilds)
		return guild

	def getRoleFromReact(self, ctx):
		guild = self.getGuild(ctx)

		for message in self.messageList: # Loop through all messages that have auto-roles
			if message == ctx.message_id: # Get message being reacted to
				for roleName in self.messageList[message]: # Check what reaction was made
					if ctx.emoji.name in self.messageList[message][roleName]:
						role = discord.utils.get(guild.roles, name=roleName)
						return role # Return associated role

	def getAllReactions(self, ctx):
		guild = self.getGuild(ctx)
		reactionList = []

		for message in self.messageList: # Loop through all messages that have auto-roles
			if message == ctx.message_id: # Get message being reacted to
				for role in self.messageList[message]: # Check what reaction was made
					reaction = self.bot.get_emoji(role[0])
					reactionList.append(reaction) # add associated role to the list
		return reactionList # Return list of all roles of that message

	def getAllRoles(self, ctx):
		guild = self.getGuild(ctx)
		roleList = []

		for message in self.messageList: # Loop through all messages that have auto-roles
			if message == ctx.message_id: # Get message being reacted to
				for emojiName in self.messageList[message]: # Check what reaction was made
					role = discord.utils.get(guild.roles, name=emojiName)
					roleList.append(role) # add associated role to the list
		return roleList # Return list of all roles of that message

	#endregion

	#region ---------------------------------------------------- VARIABLES -----------------------------------------------

	autoRoleChannelID = 864112033229570058

	messageList = {
		865634630912704512: { # Colours
			'Red': ['🔴'],
			'Orange': ['🟠'],
			'Yellow': ['🟡'],
			'Green': ['🟢'],
			'Al Green': [863637729661288458, 'dral_circle'], # 4bc84b
			'Turquoise': [863635986680512563, 'turquoise_circle'], #
			'Pink': [863628189589831700, 'pink_circle'], #
			'Lavender': ['🟣'],
			'Blue': ['🔵'],
			'Dark Blue': [863635959547035678, 'dark_blue_circle'], #
			'Dova': [863636010240180224, 'dova_circle'], # 4F6571
			'Slate': [863633806006157382, 'slate_circle'], # 0f3341
			'Franny Blue': [870266093418197003, 'franny_circle'] # 2878c0
		},
		865635642071318539: { # Games
			'minecraft cringe': [865627536854745118, 'Minecraft'],
			'War Wame': [865627466512728116, 'Warframe'],
			'dunk stunk': [865627391250399232, 'DarkSouls'],
			'Paradox Tree Fellers': [865627512398675981, 'Stellaris'],
			'CS Guys': [865627808252690502, 'CSGO'],
			'Amogus': [814738275163308052, 'sus'],
			'Group Fortification The 2nd': [865627373004652554, 'TF2'],
			'Booty Boys': [859771062916481024, 'SeaofThievespng'],
			'Factorio': [865594340126883850, 'Factorio'],
			'GTA': [881837404338651176, 'GTA']
		}
	}

	#endregion

	#region ----------------------------------------------------- EVENTS -------------------------------------------------

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, ctx):											# React to message
		if ctx.user_id == self.bot.user.id or ctx.message_id not in self.messageList:
			return

		if ctx.message_id in self.messageList:
			print('AutoRole:', ctx.member, 'has added a reaction:', ctx.emoji.name)

		guild = self.getGuild(ctx)
		member = ctx.member
		role = self.getRoleFromReact(ctx) # get selected role
		channel = self.bot.get_channel(self.autoRoleChannelID)
		message = await channel.fetch_message(ctx.message_id)
		roleType = message.embeds[0].fields[1].value

		if member is not None: # if user is found
			if role is not None: # if roles is found
				if roleType == 'Unique':
					roleList = self.getAllRoles(ctx) # Get all roles
					for oldRole in roleList: # go through every role
						if oldRole in member.roles: # if the user has a role already
							reaction = self.messageList[message.id][oldRole.name][0] # get reaction name
							await member.remove_roles(oldRole) # Remove that role from member
							
							emojiName = self.messageList[message.id][oldRole.name][0] # get reaction emoji
							if type(emojiName) == int:
								emojiName = self.bot.get_emoji(emojiName)
							await message.remove_reaction(emojiName, member) # removes reaction
							print('AutoRole: Removed old role', oldRole.name)

				await member.add_roles(role) # Add desired role
				print('AutoRole:', role.name, 'Role was given to', member.name)
			else:
				print('AutoRole: Role not found. Removing reaction')
				await message.remove_reaction(ctx.emoji, member)
		else:
			print('AutoRole: Member not found!')

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, ctx):										# Remove react from message
		guild = self.getGuild(ctx)
		member = discord.utils.find(lambda m : m.id == ctx.user_id, guild.members)
		role = self.getRoleFromReact(ctx)
		
		if ctx.message_id in self.messageList:
			print('AutoRole', member.name, 'has removed a reaction:', ctx.emoji.name)

		if role is not None:
			if member is not None:
				await member.remove_roles(role)
				print('AutoRole: Role', role.name, 'taken from', member.name)
			else:
				print('AutoRole: Member not found!')

	#endregion

	#region ----------------------------------------------------- COMMANDS -------------------------------------------------

	@commands.command()
	async def gamesSetup(self, ctx):													# gamesSetup command
		if self.admin(ctx): # if posted by me
			channel = self.bot.get_channel(self.autoRoleChannelID)
			commandMessage = await channel.fetch_message(channel.last_message_id)
			await commandMessage.delete()
			
			embed = discord.Embed (
				title='Game Roles',
				description='React to the games you want to be notified about!',
				colour=discord.Colour.blue()
			)
			embed.add_field(name="Role Options:", value="• Minecraft\n• Warframe\n• Dark Souls\n• Stellaris\n• CSGO\n• Among Us\n• TF2\n• Sea of Thieves\n• Factorio", inline=False)
			embed.add_field(name="Role Type", value="Not Unique", inline=False)
			# embed.set_footer(text='Unique')
			msg = await ctx.send(embed=embed)

			channel = self.bot.get_channel(self.autoRoleChannelID)
			message = await channel.fetch_message(channel.last_message_id)

			for role in self.messageList[865635642071318539]: # Loop through emojis
				emoji = self.messageList[865635642071318539][role][0]
				if type(emoji) == int:
					emoji = self.bot.get_emoji(emoji)
				await message.add_reaction(emoji)
		else:
			print('Not Admin!') # not posted by me

	@commands.command()
	async def colourSetup(self, ctx):													# coloursSetup command
		if self.admin(ctx): # if posted by me
			channel = self.bot.get_channel(self.autoRoleChannelID)
			commandMessage = await channel.fetch_message(channel.last_message_id)
			await commandMessage.delete()
			
			embed = discord.Embed (
				title='Colour Roles',
				description='React to the emoji to change your name colour!',
				colour=discord.Colour.blue()
			)
			embed.add_field(name="Role Options:", value="• Red\n• Orange\n• Yellow\n• Green\n• Al Green\n• Turquoise\n• Pink\n• Lavender\n• Blue\n• Dark Blue\n• Dova\n• Slate", inline=False)
			embed.add_field(name="Role Type", value="Unique", inline=False)
			# embed.set_footer(text='Unique')
			msg = await ctx.send(embed=embed)

			channel = self.bot.get_channel(self.autoRoleChannelID)
			message = await channel.fetch_message(channel.last_message_id)

			for role in self.messageList[865634630912704512]: # Loop through emojis
				emoji = self.messageList[865634630912704512][role][0]
				if type(emoji) == int:
					emoji = self.bot.get_emoji(emoji)
				await message.add_reaction(emoji)
		else:
			print('Not Admin!') # not posted by me

	#endregion

def setup(bot):
	bot.add_cog(AutoRole(bot))
