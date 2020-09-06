import os

import discord, requests

from db import get_history_keyword, store_search_history

client = discord.Client()


@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')
	return True


@client.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to my {member.dm_channel} server!'
	)
	return True


@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content == 'hi':
		await message.channel.send("hey")
	if message.content.startswith('!recent '):
		search_recent_word_key = message.content.replace('!recent ', '')
		msg =get_history_keyword(search_recent_word_key,message.author)
		print(msg)
		if msg:
			await message.channel.send(msg,delete_after=10)
		else:
			await message.channel.send("No words searched by you like `{}`!".format(search_recent_word_key),delete_after=2)
		
	elif message.content.startswith('!google_search_key '):
		key = message.content.replace('!google_search_key ', '')
		os.environ['{}_google_key'.format(message.channel)] = key
		await message.delete()
		await message.channel.send("Your key is set for this channel!")

	elif message.content.startswith('!google ') or message.content.startswith('!Google ') or message.content.startswith(
			'!GOOGLE '):
		if not os.getenv('{}_google_key'.format(message.channel)):
			await message.channel.send("Your search key is not set, please send key starts with `!google_search_key `")
		else:
			search_query = message.content.replace('!google ', '').replace('!Google ', '').replace('!GOOGLE ', '').strip()
			key = os.getenv('{}_google_key'.format(message.channel))
			print('key', key)
			cx = '67cb10efe48ca0fa2'
			result = requests.get(
				"https://www.googleapis.com/customsearch/v1?key={}&q={}&cx={}".format(key, search_query, cx))
			if result.status_code == 200:
				items = result.json().get('items')
				if len(items) < 1:
					await message.channel.send('No item found')
				else:
					embed_list = [
						discord.Embed(title = item.get('title'), url = item.get('link'), description = item.get('snippet'))
						for item in items[:5]]
					await message.channel.send('Your search results are following:')
					for embed in embed_list:
						await message.channel.send(embed = embed)
					store_search_history(search_query, message.author)
			
			else:
				await message.channel.send('No item found')
	return True