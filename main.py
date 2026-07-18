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

with open("trivia_questions_list.json", "r", encoding="utf-8") as f:
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

convo_starters = [
    "Who's a niche hear me out?",
    "What's a random food you like?",
    "What's somewhere you've been that surprised you?",
    "What are you most looking forward too?",
    "What's a niche hobby that you have?",
    "What was your screen time yesterday?",
    "What was the last song you listened to?",
    "What do you do to get rid of stress?",
    "What is something you're obsessed with?",
    "What 3 words best describe you?",
    "What's your favourite number and why?",
    "What would be your perfect day? Where would you go?",
    "What's your favourite way to waste time?",
    "What are you going to do this weekend?",
    "Thoughts on tattoos?",
    "Do you have any pets?",
    "Cats or dogs?",
    "What's something popular that you don't like?",
    "Where did you last go on holiday?",
    "When was the last time you worked really hard?",
    "What's something you've done recently that you're proud of?",
    "Do you do any sports? What's your favourite?",
    "What song best describes you?",
    "Have you ever saved someones life? Even an animal?",
    "If you could own any animal what would it be?",
    "What were you into when you were a kid?",
    "How tidy is your room right now?",
    "Who's your favourite actor?",
    "What's the weirdest dream you've had?",
    "Are you very organized?",
    "Do you like public speaking?",
    "What's one controversial opinion that you have?",
    "What's an annoying habit people have?",
    "Where's the most beautiful place you've been?",
    "What do you do with most of your spare time?",
    "How often do you stay up past 3am?",
    "What time do you usually sleep?",
    "What's your favourite season and why?",
    "Would you rather have a dream car or dream house?",
    "What insect do you hate the most?",
    "What do you bring with you everywhere you go?",
    "What's the most disgusting habit people have?",
    "What's a niche thing that really pisses you off?",
    "Who's the most famous person you've met?",
    "If you could know one thing about your future, what would it be?",
    "What's your guilty pleasure?",
    "Has anyone ever saved your life?",
    "How often do you swear?",
    "What's a silly fear you have?",
    "What's one thing you want to acomplish before you die?",
    "What's the best room in your house?",
    "Have you ever kissed someone?",
    "What's a smell you really like?",
    "What's a good dog name?",
    "What's a good cat name?",
    "How often do you help others?",
    "What's a niche talent you have?",
    "What makes you nervous?",
    "Can you speak any other languages?",
    "Who's the funniest person you've met?",
    "What was the best birthday gift you've received?",
    "What's your favourite TV show?",
    "What's your favourite movie?",
    "How often do you binge watch movies?",
    "What is really overrated?",
    "Books or movies?",
    "Do you cry to movies?",
    "Favourite genre of film/TV?",
    "What was the last concert you went to?",
    "If you could only keep 4 apps, what would they be?",
    "Most useful app on your phone?",
    "iPhone or Android?",
    "Texting or calling?",
    "Thoughts on fast food?",
    "Favourite cuisine of food?",
    "Thoughts on planes?",
    "City holiday or beach holiday?",
    "Where do you want to travel next?",
    "Opinions on AI?",
    "What do you wish was illegal?",
    "Favourite snacks?",
    "Are you any good at art/drawing?",
    "Thoughts on clowns?",
    "Do you listen to music in the shower?",
    "Favourite month?",
    "Relatable song lyric?"
]

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
    # "leah": "leah is my one and only true love i love leah omg leah mention my wife",
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
    
@bot.command()
async def convo(ctx):
    convoStarter = random.choice(convo_starters)
    await ctx.send(convoStarter)

bot.run(DISCORD_TOKEN)
