import discord
from discord.ext import commands
import asyncpg
import sys
import os
import aiohttp


class AnimeBotBeta(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=["ovovo "],
            max_messages=1000,
            intents=discord.Intents.all(),
            description="""
```
 _____ _               _          _                  ____        _   
|_   _| |__   ___     / \   _ __ (_)_ __ ___   ___  | __ )  ___ | |_ 
  | | | '_ \ / _ \   / _ \ | '_ \| | '_ ` _ \ / _ \ |  _ \ / _ \| __|
  | | | | | |  __/  / ___ \| | | | | | | | | |  __/ | |_) | (_) | |_ 
  |_| |_| |_|\___| /_/   \_\_| |_|_|_| |_| |_|\___| |____/ \___/ \__|
                                                                     
 ____       _        
| __ )  ___| |_ __ _ 
|  _ \ / _ \ __/ _` |
| |_) |  __/ || (_| |
|____/ \___|\__\__,_|
                     
```
""",
            chunk_guilds_at_startup=True,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions.none(),
            strip_after_prefix=True,
        )
    def run(self, *args, **kwargs):
        self.session = aiohttp.ClientSession(
        headers={
            "User-Agent": f"python-requests/2.25.1 The Anime Bot Beta/1.1.0 Python/{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} aiohttp/{aiohttp.__version__}"
        },
    )
        db = self.loop.run_until_complete(
            asyncpg.create_pool(
                host="localhost",
                port="5432",
                user="postgres1",
                password="postgres",
                database="animebotbeta",
                min_size=10,
                max_size=20,
            )
        )
        self.db = db
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                self.load_extension(f"cogs.{file[:-3]}")
        super().run(*args, **kwargs)