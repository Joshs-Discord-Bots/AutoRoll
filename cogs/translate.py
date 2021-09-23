
@bot.command()
async def translate(ctx, type='scramble'):
	
	
	from deep_translator import GoogleTranslator
	import random
	
	defs = {
		641549261527449611: 'secret society important',
		862669359784263700: 'GregTech General',
		862637452555190282: 'gt general',
		862668241336008724: 'Gregory Techory',
		710425685356838926: 'The Interview room',
		849349215695798333: 'The Tavern',
		820692144338632804: 'amogus',
		849349771058741258: 'Late Night Mumble Hours',
		708987349845016616: 'Uni Chat',
		806836807932706826: 'hamgouts',
		870598207443468319: 'fake bot commands',
		868315809058029619: 'Events',
		880355797580775486: 'Warframe',
		870595182104551456: 'Welcome',
		862668756273594398: 'Base Inspiration',
		870597883626389544: 'Fake General',
		842610695505969163: 'Brazil',
		863459039652478976: 'Voting',
		760832343891116104: 'Minecraft',
		849344801924448276: 'Announcements',
		835809751044587520: 'Factorio',
		331356911649685507: 'Bot Commands',
		761145006505328650: 'Stellaris',
		822814122701226024: 'Homebrewed Memes',
		864112033229570058: 'Auto-roles',
		849349370948091905: 'The Bar',
		330974948870848512: 'General',
		868316876067979294: 'Welcome',
		868315126632153158: 'court room',
		641548249630769174: 'Secret Society of Gamers',
		641549795202433047: 'secret-society-general',
		779968062270996551: 'paradox games',
		870598113079996458: 'Fake Stuff',
		849349578720804870: 'Unisex toilet',
		862905630150885406: 'To-do',
		849349433573376030: 'Upstairs',
		675661723830845440: 'camping-boys',
		752722922845503578: 'Ark fellas',
		760830073942310943: 'Gamers',
		870598022596284496: 'Fake Voice',
		641549161795158026: 'secret-society-bot-commands',
		879284789155340290: 'The Funny Lounge',
		623413680662380554: 'General'
	}


	langs = {'af': 'Afrikaans', 'ga': 'Irish', 'sq': 'Albanian', 'it': 'Italian', 'ar': 'Arabic', 'ja': 'Japanese', 'az': 'Azerbaijani', 'kn': 'Kannada', 'eu': 'Basque', 'ko': 'Korean', 'bn': 'Bengali', 'la': 'Latin', 'be': 'Belarusian', 'lv': 'Latvian', 'bg': 'Bulgarian', 'lt': 'Lithuanian', 'ca': 'Catalan', 'mk': 'Macedonian', 'zh-CN': 'Chinese Simplified', 'ms': 'Malay', 'zh-TW': 'Chinese Traditional', 'mt': 'Maltese', 'hr': 'Croatian', 'no': 'Norwegian', 'cs': 'Czech', 'fa': 'Persian', 'da': 'Danish', 'pl': 'Polish', 'nl': 'Dutch', 'pt': 'Portuguese', 'en': 'English', 'ro': 'Romanian', 'eo': 'Esperanto', 'ru': 'Russian', 'et': 'Estonian', 'sr': 'Serbian', 'tl': 'Filipino', 'sk': 'Slovak', 'fi': 'Finnish', 'sl': 'Slovenian', 'fr': 'French', 'es': 'Spanish', 'gl': 'Galician', 'sw': 'Swahili', 'ka': 'Georgian', 'sv': 'Swedish', 'de': 'German', 'ta': 'Tamil', 'el': 'Greek', 'te': 'Telugu', 'gu': 'Gujarati', 'th': 'Thai', 'ht': 'Haitian Creole', 'tr': 'Turkish', 'iw': 'Hebrew', 'uk': 'Ukrainian', 'hi': 'Hindi', 'ur': 'Urdu', 'hu': 'Hungarian', 'vi': 'Vietnamese', 'is': 'Icelandic', 'cy': 'Welsh', 'id': 'Indonesian', 'yi': 'Yiddish'}
	server = ctx.guild
	
	if type in ['restore', 'revert', 'fix']:
		if ctx.author.id == 206303139203121152:
			await ctx.send('No.')
			return
		await ctx.send('Resetting server names...')
		print('Fixing...')
		for channel in server.channels:
			if channel.id in defs:
				await channel.edit(name=defs[channel.id])
				print('Fixed', channel.name)
		clear()
		print('Restoration complete.')
		await ctx.send('Restoration complete.')

	elif type == 'scramble':
		# lang = random.choice(langs)
		lang = random.choice(list(langs.keys()))

		await ctx.send(f'Translating to {langs[lang]} and back...')
		
		for channel in server.channels:
			name = channel.name.replace('-', ' ')
			translated = GoogleTranslator(source='auto', target=lang[1]).translate(channel.name)
			translated = GoogleTranslator(source='auto', target='en').translate(translated)
			await channel.edit(name=translated)
			print(f'{name} -> {translated}')
		
		await ctx.send('Translation complete!')
		clear()
		print('Translation complete!')
	elif type in langs:
		await ctx.send(f'Translating to {langs[type]}...')
		
		for channel in server.channels:
			name = channel.name.replace('-', ' ')
			translated = GoogleTranslator(source='auto', target=type).translate(channel.name)
			await channel.edit(name=translated)
			print(f'{name} -> {translated}')
		
		await ctx.send('Translation complete!')
		
	
	else:
		await ctx.send('Usage: .translate <scramble/fix/country_code')
