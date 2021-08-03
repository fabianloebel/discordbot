from discord.ext import commands
from pystemd.systemd1 import Unit


class GameSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='state', help='Gets server state.')
    async def _get_service_state(self, ctx: commands.Context, *, service: str):
        service = service.decode("utf8", "ignore")

        async with ctx.typing():
            if service in ["vhserver", "sauerbraten-server", "cod4server", "dungeoncrawler"]:
                unit = Unit(bytes(f'{service}.service', encoding='utf-8'))
                unit.load()

                await ctx.send(f'[{service}] {unit.Unit.ActiveState}')



