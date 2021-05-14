import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from random import random

class Greeter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._members = {}
        self._greets = ['Hello ..', 'Heeeelloooo', 'Haudi', 'Servus', 'Salut', 'Hi', 'Hiiiiii', '(╯°□°）╯︵ ┻━┻']

    @commands.Cog.listener()
    async def _on_member_join(member):
        """Greets new member"""
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command(name='hello', help='Says hello.')
    async def _hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author

        if member.id not in self._members:
            self._members[member.id] = 1
            await ctx.send(f'Hello {member.name}.')

        elif self._members[member.id] == 9:
            msg = f'That\'s it {member.name}, {self._members[member.id]+1} times is once too many .. ' \
                  f'I am just going to forget that I know you!'
            await ctx.send(msg)
            del self._members[member.id]

        else:
            self._members[member.id] += 1
            await ctx.send(random.choices(self._greets)+f' {member.name}')

        if len(self._members) >= 30:
            await ctx.send(f' Too many people to memorize all of your .. I\'m just going to forget y\'all exist')
            self._members = {}

    @commands.command(name='bot', help='Gives general info about the bot.')
    async def _bot(self, ctx, *, member: discord.Member = None):
        """Prints info on bot in general"""

        load_dotenv()
        client_id = os.getenv('CLIENT_ID')
        permissions = 271969376
        url = f'https://discord.com/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot'

        # TODO use discord.utils.outh_url to auto generate URL

        msg = 'This bot can stream music from youtube! \n' \
              ' To add it to your server you can use the following invite url: \n'
        msg += url
        await ctx.send(msg)

