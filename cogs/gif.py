import os
import discord
import random
import requests
from discord.ext import commands
from dotenv import load_dotenv

def setup(bot: commands.Bot):
        bot.add_cog(Gif(bot))

class Gif(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    def get_gif(self, search = "Unicorn"):
        load_dotenv()
        tenor_token = os.getenv('TENOR_TOKEN')
        
        search_term = search #.content.lower()[5:]

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
    async def _gif(self, ctx: commands.Context, *, search = "Unicorn"):
        """ Gif stuff """
        gif_url = self.get_gif(search) #Collects word after !gif

        embed = discord.Embed(title=f"Tenor GIF", description=f"Search term: {search}",)
        embed.set_image(url=gif_url)
        await ctx.send(embed=embed)
