# Discord bot

This bot is derived from the [GodecBot](https://github.com/Lenart12/GodecBot) and can:
* Greet new members
* Play music from youtube
* Parse Spotify song and playlist links

# Setup

## Requirements

All the requirements are listed in the `requirements` file.
They can be installed directly or in a [venv](https://docs.python.org/3/library/venv.html) with:

Direct installation:

`pip3 install -r requirements`

Installation in a virtual environment (RECOMMENDED):

`python3 -m venv /path/to/venv`
`source /path/to/venv/bin/activate`
`pip3 install -r requirements`

Next to those requirements you also need ffmpeg installed on the machine that is running the bot:

### ffmpeg Linux

Install with your package manager:

Ubuntu: `sudo apt install ffmpeg`  
Arch: `sudo pacman -S ffmpeg`  

### ffmpeg Windows 

* Download prebuilt: https://www.gyan.dev/ffmpeg/builds/
    * Move download to some preferred path
    * [Add said path to PATH in Windows](https://docs.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14))

## Creating a Token

https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token

## Providing secrets

The token and the guild (aka the discord server name) have to be provided over a file called `.env` in the same directory as the bot.

Its contents have to be:  
  
`DISCORD_TOKEN=<TOKEN>`   

`DISCORD_GUILD=<GUILD_NAME>`

For spotify link support a client ID and secret are also needed:  

`SPOTIFY_CLIENT_ID=<ID>`  

`SPOTIFY_CLIENT_SECRET=<SECRET>`  

# Start

If the requirements are installed directly:  

`python3 /path/to/bot.py`  

If the requirements were installed in a virtual environment:  

`/path/to/venv/bin/python3 /path/to/bot.py`  

# Sources

The music player part:  
- https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d

Same thing but more functionality:
- https://github.com/Lenart12/GodecBot


