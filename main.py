import discord
from discord.ext import commands
import os
import re
import json
import random

import sys
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

with open("trivia_questions_6500.json", "r", encoding="utf-8") as f:
    trivia_questions = json.load(f)

current_question = None

def normalise_answer(text):
    text = text.lower().strip()
    text = re.sub(r"^answer\s*:\s*", "", text)
    return text

leah_user_id = 1283126859810209886

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents)

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
    # "hello": "hello! (in japanese~)",
    # "hi": "hello! (in japanese~)",
    # "hii": "hello! (in japanese~)",
    # "daddy": "gulp 😳",
    # "dada": "not sure im ready for that yet HA HA HA",
    # "dadda": "not sure im ready for that yet HA HA HA",
    # "sobbing": "dont cry! im here ;)",
    # "crine": "dont cry! im here ;)",
    # "rodrigo": "im better btw 😝",
    # "laufey": "laufey mention",
    # "neco": "neco williams my beloved",
    "arisu": "me mention",
    "in borderland": "who in borderland? 😳",
    "aib": "who in borderland? 😳",
    # "son": "hi i dont know what to say im just here 😉",
    # "help": "what do you need 😙",
    # "helpp": "what do you need 😙",
    "chud": "im a chud im a chud im a fat little chud",
    # "fav food": "pizza idk",
    # "fav show": "alice in borderland duh 🤣",
    # "nope": "YUP!",
    # "nopee": "YUP!",
    # "gay": "im gay",
    "67": "SIX SEVENN",
    # "bye": "no come back 😘🫦",
    # "goodnight": "goodnight~",
    # "gn": "goodnight~",
    # "gnn": "goodnight~",
    # "ride": "😳😏",
    # "japan": "japan mention thats where im from",
    # "tuff": "im tuffer",
    # "hannah": "i agree with mimu!!",
    "leah": "leah is my one and only true love i love leah omg leah mention my wife",
    # "happy": "im happy all the time but only when im with leah"
}

special_replies = {
    
}

disabled_channels = [
    1509691580666347610
]

last_trivia = {}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

    if message.channel.id in disabled_channels:
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
    
    if message.channel.id in last_trivia:
        question = last_trivia[message.channel.id]

        user_answer = normalise_answer(message.content)
        correct_answer = normalise_answer(question["a"])

        if user_answer == correct_answer:
            await message.channel.send(f"Well done! The answer is {question['a']}")
            del last_trivia[message.channel.id]

@bot.command()
async def trivia(ctx):
    question = random.choice(trivia_questions)
    last_trivia[ctx.channel.id] = question
    await ctx.send(question["q"])

@bot.command()
async def skip(ctx):
    question = random.choice(trivia_questions)
    last_trivia[ctx.channel.id] = question
    await ctx.send(question["q"])

@bot.command()
async def answer(ctx):
    if ctx.channel.id not in last_trivia:
        await ctx.send("No active trivia question!")
        return

    question = last_trivia.pop(ctx.channel.id)
    await ctx.send(f"Answer: {question['a']}")
    

bot.run(DISCORD_TOKEN)
