import discord
from discord.ext import commands
import os
import re

import sys
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

leah_user_id = 1283126859810209886

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

    await bot.change_presence(
        activity=discord.Game("i am daddy arisu"),
        status=discord.Status.online
    )

    print(f"Logged in as {bot.user}")

responses = {
    "hello": "hello! (in japanese~)",
    "hi": "hello! (in japanese~)",
    "hii": "hello! (in japanese~)",
    "daddy": "gulp 😳",
    "dada": "not sure im ready for that yet HA HA HA",
    "dadda": "not sure im ready for that yet HA HA HA",
    "sobbing": "dont cry! im here ;)",
    "crine": "dont cry! im here ;)",
    "rodrigo": "im better btw 😝",
    "laufey": "laufey mention",
    "neco": "neco williams my beloved",
    "arisu": "me mention",
    "in borderland": "who in borderland? 😳",
    "son": "hi i dont know what to say im just here 😉",
    "help": "what do you need 😙",
    "helpp": "what do you need 😙",
    "chud": "im a chud im a chud im a fat little chud",
    "fav food": "pizza idk",
    "fav show": "alice in borderland duh 🤣",
    "nope": "YUP!",
    "nopee": "YUP!",
    "gay": "im gay",
    "67": "SIX SEVENN",
    "bye": "no come back 😘🫦",
    "goodnight": "goodnight~",
    "gn": "goodnight~",
    "gnn": "goodnight~",
    "ride": "😳😏",
    "japan": "japan mention thats where im from",
    "tuff": "im tuffer",
    "hannah": "i agree with mimu!!",
    "leah": "leah is my one and only true love i love leah omg leah mention my wife",
    "happy": "im happy all the time but only when im with leah"
}

special_replies = {
    
}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.author.id in special_replies:
        await message.channel.send(special_replies[message.author.id])
    
    content = message.content.lower()

    replies = []

    for trigger, response in responses.items():
        if re.search(rf"\b{re.escape(trigger)}\b", content):
            replies.append(response)
    for reply in replies:
        await message.channel.send(reply)

bot.run(DISCORD_TOKEN)