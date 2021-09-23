import discord
from discord.ext import commands
import yaml
#import AutoRole

class FunnyScore(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	filename = 'funny_stats.yaml'
	autoReact = True
	xp_filename = 'xp_stats.yaml'
	prices = {'send': 5, 'react': 1}
	
	def isMeme(self, message):
		memeFlags = ['twitter.com', 'discordapp', 'tenor.com', 'tumblr', 'youtube.com']
		for flag in memeFlags:
			if message.attachments or flag in message.content:
				return True
		return False

	def read(self, readFilename):
		try:
			with open(readFilename) as f:
				return yaml.load(f, Loader=yaml.FullLoader)
		except FileNotFoundError:
			return None

	def write(self, data, writeFilename):
		with open(writeFilename, 'w') as f:
			data = yaml.dump(data, f)
		return

	

'''
	# ---------------------------------------------------------------------------------------------------------

	@commands.command()
	async def funnyScore(self, ctx, user: discord.Member = None):
		if user == None: # if user doesnt spesify user, default to author
			user = ctx.author

		data = self.read(self.filename)
		
		if data == None: # No data recorded
			await ctx.send('There is no data!')
			return

		if user.id not in data: # Requested user has no data
			embed = discord.Embed (
			title=f"{user.name}'s Meme Stats",
			description=f'No Data Available!',
			colour=discord.Colour.blue()
			)
			msg = await ctx.send(embed=embed)
			return

		memeTotal = posTotal = negTotal = 0 # Template
		for meme in data[user.id]: # Total likes/dislikes
			memeTotal+=1
			if data[user.id][meme]['weight'] > 0:
				posTotal+=1
			elif data[user.id][meme]['weight'] < 0:
				negTotal+=1
		funnyScore = round((posTotal/memeTotal)*100, 2) # Calculate funny
		
		embed = discord.Embed ( # Message
			title=f"{user.name}'s Meme Stats",
			description=f'Total Memes Send: {memeTotal}\nPositive Memes: {posTotal}\nNegative Memes: {negTotal}',
			colour=discord.Colour.blue()
		)
		embed.add_field(name="Funniness Score:", value=f'{funnyScore}%', inline=False)
		msg = await ctx.send(embed=embed)

	@commands.command()
	async def xp(self, ctx, user: discord.Member = None):
		if user == None: # if user doesnt spesify user, default to author
			user = ctx.author

		xp_data = self.read(self.xp_filename)
		
		if xp_data == None: # No data recorded
			await ctx.send('There is no data!')
			return

		if user.id not in xp_data: # Requested user has no data
			xp = 0
		else:
			xp = xp_data[user.id]
		
		embed = discord.Embed (
		title=f"{user.name}'s XP Stats",
		description=f'{xp} XP',
		colour=discord.Colour.blue()
		)
		await ctx.send(embed=embed)

	@commands.command()
	async def autoReact(self, ctx):
		self.bot.config = self.read('config.yaml')
		if self.bot.config['autoReact'] == True:
			await ctx.send('Auto-react has been turned `off`')
		else:
			await ctx.send('Auto-react has been turned `on`')
		self.bot.config['autoReact'] = not self.bot.config['autoReact']
		self.write(self.bot.config, 'config.yaml')
		
	@commands.command()
	async def leaderboard(self, ctx):
		leaderboard = []
		data = self.read(self.filename)
		if data == None:
			embed = discord.Embed ( # Message
			title='Funny Leaderboard',
			description=f'No data to compare!',
			colour=discord.Colour.blue()
			)
			msg = await ctx.send(embed=embed)
			return


		for user_id in data:
			memeTotal = posTotal = 0
			for meme in data[user_id]: # Total likes/dislikes
				memeTotal+=1
				if data[user_id][meme]['weight'] > 0:
					posTotal+=1
			funnyScore = round((posTotal/memeTotal)*100, 2) # Calculate funny
			user = self.bot.get_user(user_id)
			leaderboard.append([user.name, memeTotal, funnyScore])
		leaderboard.sort(key=lambda x:x[2], reverse=True)
		
		embed = discord.Embed ( # Message
			title='Funny Leaderboard',
			description=f'Showing the top 5 funniest people on the server',
			colour=discord.Colour.blue()
		)
		for i, user in enumerate(leaderboard):
			if i+1 > 5:
				break
			embed.add_field(name=f'#{i+1} {user[0]}', value=f'Memes sent: {user[1]}\nFunniness Score: {user[2]}%', inline=False)
		msg = await ctx.send(embed=embed)

	@funnyScore.error
	async def funnyScore_error(self, ctx, error):
		if isinstance(error, commands.MemberNotFound):
			await ctx.send('That user does not exist!')

	# ---------------------------------------------------------------------------------------------------------

	@commands.Cog.listener()
	async def on_message(self, message): # React to author's memes
		self.bot.config = self.read('config.yaml')
		if self.isMeme(message) and self.bot.config['autoReact']:
			await message.add_reaction(self.bot.get_emoji(872062376105607168)) # Upvote Emoji
			await message.add_reaction(self.bot.get_emoji(736841294055473212)) # Downvote Emoji
		
		if self.isMeme(message):
			data = self.read(self.xp_filename)
			if data == None:
				data = {}
			if message.author.id not in data:
				data[message.author.id] = 0
			data[message.author.id]+=self.prices['send']
			self.write(data, self.xp_filename)

	@commands.Cog.listener() # Handle reacitons
	async def on_raw_reaction_add(self, ctx):
		if ctx.user_id == self.bot.id: # Ignore bot's reactions
			return
		channel = self.bot.get_channel(ctx.channel_id) # get reacted messages' channel
		message = await channel.fetch_message(ctx.message_id) # get reacted message
		reactor_id = ctx.user_id # debastardize variable name

		if self.isMeme(message): # if reacted message is meme
			if message.author.id != reactor_id: # if msg was reacted by NOT the author
				
				xp_data = self.read(self.xp_filename)
				if ctx.user_id not in xp_data:
					xp_data[ctx.user_id] = 0
				
				data = self.read(self.filename) # read data, if empty, create
				if data == None:
					data = {}


				if xp_data[ctx.user_id] >= self.prices['react']:
					if ctx.emoji == self.bot.get_emoji(872062376105607168) or ctx.emoji == self.bot.get_emoji(736841294055473212): # Upvote

						# region				Make sure shit isnt missing
						if message.author.id not in data:
							data[message.author.id] = {}
						if message.id not in data[message.author.id]:
							meme = {'likes': 0, 'dislikes': 0, 'weight': 0, 'reactors': []}
						else:
							meme = data[message.author.id][message.id]
						# endregion
						
						if reactor_id not in meme['reactors']: # If someone new reacts, update meme stats
							print(f"FunnyScore: {ctx.member.name} has {ctx.emoji.name}d {message.author.name}'s meme")
							if ctx.emoji == self.bot.get_emoji(872062376105607168):
								meme['likes']+=1
								meme['weight']+=1
							elif ctx.emoji == self.bot.get_emoji(736841294055473212):
								meme['dislikes']+=1
								meme['weight']-=1

							meme['reactors'].append(reactor_id) # Add reactor to list
							xp_data[ctx.user_id]-=self.prices['react']
							xp_data[message.author.id]+=self.prices['react']
							data[message.author.id][message.id] = meme # bundle data
				
				else:
				
					print('no')
					cost = self.prices['react']
					botCommands = self.bot.get_channel(331356911649685507) # get reacted messages' channel
					await botCommands.send(f'Reacting costs `{cost} XP` {ctx.member.mention}!\nPost memes to earn XP')
					await message.remove_reaction(self.bot.get_emoji(872062376105607168), ctx.member) # Upvote)
					await message.remove_reaction(self.bot.get_emoji(736841294055473212), ctx.member) # Downvote)
			
				self.write(data, self.filename) # write data
				self.write(xp_data, self.xp_filename)


'''

def setup(bot):
	bot.add_cog(FunnyScore(bot))