import discord
import os
import re

import sys
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1
    print("Arisu is in " + str(guild_count) + " server(s).")

responses = {
    "hello": "hello! (in japanese~)",
    "hi": "hello! (in japanese~)",
    "daddy": "gulp",
    "dada": "not sure im ready for that yet HA HA HA",
    "dadda": "not sure im ready for that yet HA HA HA",
    "sobbing": "dont cry! im here ;)",
    "rodrigo": "im better btw",
    "laufey": "laufey mention",
    "neco": "neco williams my beloved",
    "arisu": "me mention",
    "in borderland": "who in borderland?",
    "son": "hi i dont know what to say im just here",
}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    content = message.content.lower()

    replies = []

    for trigger, response in responses.items():
        if re.search(rf"\b{re.escape(trigger)}\b", content):
            replies.append(response)
    for reply in replies:
        await message.channel.send(reply)

bot.run(DISCORD_TOKEN)