import os
import discord
import random
import requests
from discord.ext import commands
from dotenv import load_dotenv


def setup(bot: commands.Bot):
        bot.add_cog(Greeter(bot))

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
            await ctx.send(random.choice(self._greets)+f' {member.name}')

        if len(self._members) >= 30:
            await ctx.send(f' Too many people to memorize all of your .. I\'m just going to forget y\'all exist')
            self._members = {}

    @commands.command(name='about', help='Gives general info about the bot.')
    async def _about(self, ctx, *, member: discord.Member = None):
        """Prints info on bot in general"""

        load_dotenv()
        client_id = os.getenv('CLIENT_ID')
        permissions = 271969376
        url = f'https://discord.com/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot'

        # https://discord.com/oauth2/authorize?client_id=779845598068867072&permissions=271969376&scope=bot
        # TODO use discord.utils.outh_url to auto generate URL

        msg = f'This bot can stream music from youtube! \n ' \
              f'For an overview of all commands try `?help` \n\n' \
              f'To add the Partybot to your own server, you can checkout the [repository](https://gitlab.com/darktin30/tssetse-bot)!\n' \
              f'I on the other hand can just klick this link: [invite!]({url}) ;)\n'

        embed = discord.Embed(description=f'**About Partybot** \n\n {msg}')
        await ctx.send(embed=embed)

    def get_gif(search_term):
        load_dotenv()
        tenor_token = os.getenv('TENOR_TOKEN')
        
        response = requests.get("https://g.tenor.com/v1/search?q={}&key={}&limit=1".format(search_term, tenor_token))
        data = response.json()
    
        ''' 
        # see urls for all GIFs
    
        for result in data['results']:
            print('- result -')
            #print(result)
        
            for media in result['media']:
                print('- media -')
                print(media)
                print(media['gif'])
                print('url:', media['gif']['url'])
        '''
         
        return data['results'][0]['media'][0]['gif']['url']

    @commands.command(name='gif', help='Fetches gif for supplied search term')
    async def _gif(self, ctx, *, member: discord.Member = None):
        """ Gif stuff """
        gif_url = get_gif(message.content.lower()[5:]) #Collects word after !gif

        embed = discord.Embed()
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)

