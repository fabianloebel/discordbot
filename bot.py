# bot.py

import os
from dotenv import load_dotenv
import logging

import discord
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
_TOKEN = os.getenv('DISCORD_TOKEN')
_GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='?')

bot.load_extension("cogs.greeter")
bot.load_extension("cogs.music")
bot.load_extension("cogs.gamesystem")



@bot.event 
async def on_error(event, *args, **kwargs): 
    with open('err.log', 'a') as f: 
        if event == 'on_message': 
            f.write(f'Unhandled message: {args[0]}\n') 
        else: 
            raise

@bot.event
async def on_ready():
   print(f'{bot.user.name} has connected to Discord!') 

bot.run(_TOKEN)
