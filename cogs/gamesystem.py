import discord
from discord.ext import commands
from pystemd.systemd1 import Unit


class GameSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='servers', help='Gets server state.')
    async def _get_service_state(self, ctx: commands.Context):
        #service = service.decode("utf8", "ignore")

        async with ctx.typing():
            states = ""
            embed = discord.Embed(title="Server status")
            for service in ["vhserver", "sauerbraten-server", "cod4server"]:
                unit = Unit(bytes(f'{service}.service', encoding='utf-8'))
                unit.load()
                
                status = unit.Unit.ActiveState.decode("utf8")
                embed.add_field(name=service, value=status, inline=True)

            await ctx.send(embed=embed)



