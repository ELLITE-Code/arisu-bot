import discord
import os

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
    "daddy": "gulp"
}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    content = message.content.lower()

    for trigger, response in responses.items():
        if trigger in content:
            await message.channel.send(response)
            break

bot.run(DISCORD_TOKEN)