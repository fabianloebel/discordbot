from discord.ext import commands
from pystemd.systemd1 import Unit
from dotenv import load_dotenv
import subprocess
import discord
import os


def setup(bot: commands.Bot):
        bot.add_cog(GameSystem(bot))

class GameSystem(commands.Cog):

    actions = {
        "start": ["sudo", "/bin/systemctl", "start"],
        "stop": ["sudo", "/bin/systemctl", "stop"],
        "restart": ["sudo", "/bin/systemctl", "restart"]
    }

    services = {
            "vhserver":"Valheim",
            "pmcserver":"Minecraft",
            "sauerbraten-server":"Sauerbraten",
            "cod4server":"CoD 4"
    }

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.services_lower = [server.lower() for server in list(self.services.values())]

    def run_command(self, service = None, action = None):
        server = None
        status = "Bonkers"

        if service in self.services.keys():
            server = service
        elif service in self.services_lower:
            server = list(self.services.keys())[list(self.services_lower).index(service)]

        if (server is not None) and (action in self.actions.keys()):
            try:
                status = subprocess.check_output(self.actions[action] + [server])
            except Exception as e:
                status = e
        else:
            status = 'Invalid server name'

        return status, server

    def get_status(self, service):
        unit = Unit(bytes(f'{service}.service', encoding='utf-8'))
        unit.load()
        status = unit.Unit.ActiveState.decode("utf8")

        print(status)
        return status

    def check_guild(self, ctx):
        load_dotenv()
        required_id = os.getenv('DISCORD_GUILD_ID') 
        current_id = str(ctx.guild.id);

        if required_id == current_id:
            return True
        else:
            print(f"Invalid guild id: Got {current_id} but required {required_id}")
            return False



    @commands.group(pass_context = True, help='Server status parent command')
    @commands.has_role("@server")
    async def server(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Usage: \n{usage}')

    @server.command()
    async def status(self, ctx:commands.Context):
        async with ctx.typing():
            embed = discord.Embed(title="Server status")
            embed.set_thumbnail(url='https://dungeoncrawler.xyz/img/favicons/favicon.png')
            for service in self.services.keys():
                status = self.get_status(service)
                embed.add_field(name=f"{self.services[service]} server", value=status, inline=False)

            await ctx.send(embed=embed)

    @server.command()
    async def stop(self, ctx:commands.Context, *, service = None):
        if not self.check_guild(ctx):
            await ctx.send(f'Invalid guild id')
            return

        async with ctx.typing():
            embed = discord.Embed(title="Server status")
            embed.set_thumbnail(url='https://dungeoncrawler.xyz/img/favicons/favicon.png') 

            status, server = self.run_command(service, "stop")
            
            if self.get_status(server) != "inactive":
                embed.add_field(name=f"Stopping {service} failed!", value=status, inline=False)
            else:
                embed.add_field(name=f"Stopping {service} succeeded!", value=f"{server} inactive", inline=False)

            await ctx.send(embed=embed)

    @server.command()
    async def start(self, ctx:commands.Context, *, service = None):
        if not self.check_guild(ctx):
            await ctx.send(f'Invalid guild id')
            return

        async with ctx.typing():
            embed = discord.Embed(title="Server status")
            embed.set_thumbnail(url='https://dungeoncrawler.xyz/img/favicons/favicon.png') 

            status, server = self.run_command(service, "start")

            if self.get_status(server) != "active":
                embed.add_field(name=f"Starting {service} failed!", value=status, inline=False)
            else:
                embed.add_field(name=f"Starting {service} succeeded!", value=f"{server} active", inline=False)

            await ctx.send(embed=embed)

    
