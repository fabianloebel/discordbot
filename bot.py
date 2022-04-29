# bot.py

import os
from dotenv import load_dotenv
import logging
import asyncio

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
bot.load_extension("cogs.gif")
bot.load_extension("cogs.music")
bot.load_extension("cogs.gamesystem")

GUILD_VC_TIMER = {}

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


@bot.event
# runs on every leave, join, defen, mute
async def on_voice_state_update(member, before, after):
    # was event triggered by bot?
    if member.id == bot.user.id:
        return
    
    # when before channel != None means usser has left a channel
    if before.channel != None:
        voice = discord.utils.get(bot.voice_clients, channel__guild__id = before.channel.guild.id)

        if voice == None:
            return

        # if voice channel left by user not equal to bot voice channel
        if voice.channel.id != before.channel.id:
            return

        # if voice channel has only 1 member (including bot)
        if len(voice.channel.members) <= 1:

            GUILD_VC_TIMER[before.channel.guild.id] = 0

            while True:
                await asyncio.sleep(1)

                GUILD_VC_TIMER[before.channel.guild.id] += 1

                # if voice channel has more than 1 member or bot already disconnected
                if len(voice.channel.members) >= 2 or not voice.is_connected():
                    break

                # if bot was alone for more than 60 sec
                if GUILD_VC_TIMER[before.channel.guild.id] >= 60:
                    await voice.disconnect()
                    return 

            

bot.run(_TOKEN)
