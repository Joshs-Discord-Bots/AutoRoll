import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
import yaml

# play
# queue
# clear
# move
# remove
# pause

# every 5 minutes, check if people in chat



class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	queueFilename = 'queue.yaml'

	def readQueue(self):
		try:
			with open(self.queueFilename) as f:
				return yaml.load(f, Loader=yaml.FullLoader)
		except FileNotFoundError:
			return None

	def writeQueue(self):
		with open(self.queueFilename, 'w') as f:
			yaml.dump(self.queue, f)
		return
	
	#----------------------------------------------------- COMMANDS -------------------------------------------------

	@commands.command()
	async def search(self, ctx, query):
		videosSearch = VideosSearch(query, limit = 1)
		vid = videosSearch.resultComponents[0]
		await ctx.send(vid['title'])
		print(videosSearch.result())

	@commands.command()
	async def join(self, ctx):
		if ctx.voice_client == None:
			if ctx.author.voice == None:
				await ctx.send('You must be in a voice channel to use this command!')
				return False
			else:
				await ctx.author.voice.channel.connect()
				return True
		else:
			await ctx.send('Bot is already in a voice channel!')

	@commands.command(aliases=['die', 'perish', 'death', 'annihilate', 'suffer', 'cease'])
	async def leave(self, ctx):
		if ctx.voice_client == None:
			await ctx.send('Bot is not in any voice channel!')
		else:
			await ctx.voice_client.disconnect()

	@commands.command(aliases=['add'])
	async def play(self, ctx, search = None):
		if ctx.voice_client == None:
			if not await self.join(ctx):
				return
		self.queue = self.readQueue()
		if self.queue == None:
			self.queue = []

		if search != None:
			video = VideosSearch(search, limit = 1).resultComponents[0]
			storeVideo = {
				'title': video['title'],
				'duration': video['duration'],
				'url': video['link']
			}
			self.queue.append(storeVideo)
			await ctx.send(f"`{video['title'][:50]}... ({video['duration']})` has been added to the queue")
		
		self.writeQueue()

	@commands.command()
	async def queue(self, ctx):
		self.queue = self.readQueue()
			
		embed = discord.Embed ( # Message
			title='Music Queue',
			colour=discord.Colour.blue()
		)
		if self.queue == None:
			embed.add_field(name='Listing songs...', value=f'There are no songs in the queue!', inline=False)
		else:
			desc = ''
			for i, song in enumerate(self.queue):
				desc+= f'`{i+1})  {song["title"][:50]}...` ({song["duration"]})\n'
			embed.add_field(name='Listing songs...', value=desc, inline=False)
		await ctx.send(embed=embed)

	@commands.command()
	async def remove(self, ctx, index = None):
		if index == None:
			ctx.send('Please select a position in the queue to remove!')
			return
		
		self.queue = self.readQueue()
		try:
			self.queue.pop(index-1)
			await ctx.send(f'Song `#{index}` has been removed from the queue')
		except:
			await ctx.send('That song could not be removed from the queue!')


def setup(bot):
	bot.add_cog(Music(bot))