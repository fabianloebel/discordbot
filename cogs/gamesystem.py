import discord
from discord.ext import commands
from pystemd.systemd1 import Unit
import subprocess

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
                status = subprocess.run(self.actions[action] + [server])
            except Exception as e:
                status = e
        else:
            status = 'Invalid server name'

        return status

    def get_status(self, service):
        unit = Unit(bytes(f'{service}.service', encoding='utf-8'))
        unit.load()
        status = unit.Unit.ActiveState.decode("utf8")
        return status

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
                status = self.get_status()
                embed.add_field(name=f"{self.services[service]} server", value=status, inline=False)

            await ctx.send(embed=embed)

    @server.command()
    async def stop(self, ctx:commands.Context, *, service = None):
        async with ctx.typing():
            
            status = self.run_command(service, "stop")
            if self.get_status(service) != "inactive":
                status = f"Stopping {service} failed: {status}"
            else:
                status = f"Stopping {service} succeeded!"

            await ctx.send(f'Server says: \n{status}')

    @server.command()
    async def start(self, ctx:commands.Context, *, service = None):
        async with ctx.typing():
            
            status = self.run_command(service, "start")
            if self.get_status(service) != "active":
                status = f"Starting {service} failed: {status}"
            else:
                status = f"Starting {service} succeeded!"


            await ctx.send(f'Server says: \n{status}')

    
