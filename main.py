import asyncio
import config
import warnings
import os
import logging
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from utils.subclasses import AnimeBotBeta

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


warnings.filterwarnings("ignore", category=DeprecationWarning)


bot = AnimeBotBeta()
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True, override_type=True)


bot.owner_ids = [711057339360477184, 590323594744168494]

os.environ["NO_COLOR"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

bot.run(config.token)