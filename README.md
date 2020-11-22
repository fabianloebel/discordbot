# First: Ignore the bot name :D

This bot can:
* Greet new members
* Play music from all sources that are supported by youtube-dl

# Setup

## Requirenments

All the requirenments are listed in the `requirenments` file.
They can be installed directly or in a [venv](https://docs.python.org/3/library/venv.html) with:

`pip3 install -r requirenments`

## Creating a Token

https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token

## Providing Token

The token and the guild (aka the discord server name) have to be provided over a file called `.env` in the same directory as the bot.

Its contents have to be:

`DISCORD_TOKEN=TOKEN` 

`DISCORD_GUILD=GUILD_NAME` 

# Start

`python3 /path/to/bot.py`

# Sources

The music player part:
- https://gist.github.com/vbe0201/ade9b80f2d3b64643d854938d40a0a2d

Same thing but more functionality:
- https://github.com/Lenart12/GodecBot


