# bot.py
import os
import random
from dotenv import load_dotenv

from discord.ext import commands 

from music import *
from greeter import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='?')

bot.add_cog(Greeter(bot))
bot.add_cog(Music(bot))

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

bot.run(TOKEN)
