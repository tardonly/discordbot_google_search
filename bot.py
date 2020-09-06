import os

import discord, requests


client = discord.Client()


@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')


@client.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to my {member.dm_channel} server!'
	)


@client.event
async def on_message(message):
	print(message.author, client.user)
	# if message.author == client.user:
	# 	return
	
	if message.content == 'hi':
		await message.channel.send("hey")
	elif message.content.startswith('google_search_key:'):
		key = message.content.replace('google_search_key:', '')
		os.environ['{}_google_key'.format(message.channel)] = key
		await message.delete()
		await message.channel.send("Your key is set for this channel!")

	elif message.content.startswith('google:') or message.content.startswith('Google:') or message.content.startswith(
			'GOOGLE:'):
		if not os.getenv('{}_google_key'.format(message.channel)):
			await message.channel.send("Your search key is not set, please send key starts with `google_search_key:`")
		else:
			search_query = message.content.replace('google:', '').replace('Google:', '').replace('GOOGLE:', '').strip()
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
						for item in items[:4]]
					await message.channel.send('Your search results are following:')
					for embed in embed_list:
						await message.channel.send(embed = embed)
			
			else:
				await message.channel.send('No item found')
