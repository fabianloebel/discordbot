# bot.py

from cogs.music import *
from cogs.greeter import *
from cogs.gamesystem import *

load_dotenv()
_TOKEN = os.getenv('DISCORD_TOKEN')
_GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='?')

bot.add_cog(Greeter(bot))
bot.add_cog(Music(bot))
#bot.add_cog(GameSystem(bot))

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
