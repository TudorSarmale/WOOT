import discord
from discord.ext import commands
import os
import asyncio
import logging
from configparser import ConfigParser

#Number of times Vadim cog loader broke and had to be rewritten: 2


configfile = "bot.ini"
config =  ConfigParser()
config.read(configfile)

handler = logging.FileHandler(filename=str(config['logging']['filename']), encoding=str(config['logging']['encoding']), mode=str(config['logging']['mode']))

bot = commands.Bot(command_prefix = str(config['bot']['command_prefix']),intents=discord.Intents().all(), activity=discord.Activity(type=discord.ActivityType.playing, name="Running Vadim Dev Build"))

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")
            

class mybot(commands.Bot):
  async def setup_hook(self):
    await load_extensions()
    
    

bot = mybot(command_prefix = str(config['bot']['command_prefix']), intents=discord.Intents().all(), activity=discord.Activity(type=discord.ActivityType.playing, name="Running Vadim Dev Build"))
bot.run(str(config['bot']['bot_token']),log_handler=handler)
