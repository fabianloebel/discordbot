import asyncio
import functools

import discord
import yt_dlp
from discord.ext import commands

yt_dlp.utils.bug_reports_message = lambda: ''

def extract_only(webpage_url, ytdl_options):
    with yt_dlp.YoutubeDL(ytdl_options) as ydl:
        return ydl.extract_info(webpage_url, download=False)

def search_extract_only(search, ytdl_options):
    with yt_dlp.YoutubeDL(ytdl_options) as ydl:
        return ydl.extract_info(search, download=False, process=False)

class YTDLError(Exception):
    pass

class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'default_search': 'ytsearch',
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'source_address': '0.0.0.0',
    }

    YTDL_STREAM_OPTIONS = {
        **YTDL_OPTIONS,
        'noplaylist': True,
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
    }

    YTDL_SEARCH_OPTIONS = {
        **YTDL_OPTIONS,
        'noplaylist': False,
        'extractaudio': False,
        'extract_flat': True,
        'no_warnings': True,
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        urls_to_play = []
        cls_to_play = []

        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(None, search_extract_only, search, cls.YTDL_STREAM_OPTIONS)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            # Case for normal Youtube videos
            process_info = data
            urls_to_play.append(process_info['webpage_url'])
        else:
            # Case for Youtube playlists
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    # Returned JSON has no key 'webpage_url', but rather the Video ID accessible at key 'url'
                    #urls_to_play.append("https://www.youtube.com/watch?v="+process_info['url'])
                    urls_to_play.append(process_info['url'])

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        for webpage_url in urls_to_play:
            processed_info = await loop.run_in_executor(None, extract_only, webpage_url, cls.YTDL_STREAM_OPTIONS)

            if processed_info is None:
                raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

            # Highly verbose output of accessed content!
            #print(processed_info)

            if 'entries' not in processed_info:
                info = processed_info
            else:
                info = None
                while info is None:
                    try:
                        info = processed_info['entries'].pop(0)
                    except IndexError:
                        raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))
            cls_to_play.append(cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info))
        return cls_to_play

    @classmethod
    async def search_source(cls, bot: commands.Bot, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        channel = ctx.channel
        loop = loop or asyncio.get_event_loop()
        nr_recommendations = 10
        cls.search_query = '%s%s:%s' % ('ytsearch', nr_recommendations, ''.join(search))

        data = await loop.run_in_executor(None, extract_only, cls.search_query, cls.YTDL_SEARCH_OPTIONS)

        cls.search = {}
        cls.search["title"] = f'Search results for:\n**{search}**'
        cls.search["type"] = 'rich'
        cls.search["color"] = 7506394
        cls.search["author"] = {'name': f'{ctx.author.name}', 'url': f'{ctx.author.avatar_url}', 'icon_url': f'{ctx.author.avatar_url}'}
        
        lst = []

        for e in data['entries']:
            lst.append(f'`{data["entries"].index(e) + 1}.` [{e.get("title")}]({e.get("url")})\n')

        lst.append('\n**Type a number to make a choice, Type `cancel` to exit**')
        cls.search["description"] = "\n".join(lst)

        em = discord.Embed.from_dict(cls.search)
        await ctx.send(embed=em, delete_after=45.0)

        def check(msg):
            return msg.content.isdigit() == True and msg.channel == channel or msg.content == 'cancel' or msg.content == 'Cancel'
        
        try:
            m = await bot.wait_for('message', check=check, timeout=45.0)

        except asyncio.TimeoutError:
            ret = 'timeout'

        else:
            if m.content.isdigit() == True:
                sel = int(m.content)
                if 0 < sel <= nr_recommendations:
                    entry = data['entries'][sel-1]
                    VUrl = entry['url']
                    info = await loop.run_in_executor(None, extract_only, VUrl, cls.YTDL_STREAM_OPTIONS)
                    ret = cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)
                else:
                    ret = 'sel_invalid'
            elif m.content == 'cancel':
                ret = 'cancel'
            else:
                ret = 'sel_invalid'
        
        return ret

    @staticmethod
    def parse_duration(duration: int):
        if duration > 0:
            minutes, seconds = divmod(duration, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)

            duration = []
            if days > 0:
                duration.append('{}'.format(days))
            if hours > 0:
                duration.append('{}'.format(hours))
            if minutes > 0:
                duration.append('{}'.format(minutes))
            if seconds > 0:
                duration.append('{}'.format(seconds))
            
            value = ':'.join(duration)
        
        elif duration == 0:
            value = "LIVE"
        
        return value
