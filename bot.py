import os
import discord
import dotenv
import datetime
import re

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHAN_MAX_LEN = 32

intents = discord.Intents.default()
intents.guild_scheduled_events = True
intents.members = True
client = discord.Client(intents=intents)

def to_channel_name(str):
	event_name = re.sub(r'[^a-z ]', '', str.lower()).split(' ')
	chan_name = []
	name_len = 0
	for c in event_name:
		if len(c) == 0:
			pass
		elif len(c) + name_len < CHAN_MAX_LEN:
			chan_name.append(c)
			name_len += len(c)
		else:
			break
	return '-'.join(chan_name)
	
def get_category(guild, name):
	for c in guild.categories:
		if c.name == name:
			return c

def get_channel_in_category(category, name):
	for c in category.text_channels:
		if c.name == name:
			return c

def get_member(guild, user):
	for m in guild.members:
		if m.id == user.id:
			return m

@client.event
async def on_ready():
	print(f'Logged on as {client.user}.')

@client.event
async def on_scheduled_event_create(event):
	new_channel = await get_category(event.guild, "Concerts").create_text_channel(to_channel_name(event.name))
	await new_channel.set_permissions(get_member(event.guild, event.creator), read_messages=True)

@client.event
async def on_scheduled_event_user_add(event, user):
	await get_channel_in_category(get_category(event.guild, "Concerts"), to_channel_name(event.name)).set_permissions(get_member(event.guild, user), read_messages=True)

@client.event
async def on_scheduled_event_user_remove(event, user):
	await get_channel_in_category(get_category(event.guild, "Concerts"), to_channel_name(event.name)).set_permissions(get_member(event.guild, user), read_messages=False)

@client.event
async def on_scheduled_event_delete(event):
	await get_channel_in_category(get_category(event.guild, "Concerts"), to_channel_name(event.name)).delete()

client.run(TOKEN)
