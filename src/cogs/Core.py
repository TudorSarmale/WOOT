import discord
from discord.ext import commands
import time
from datetime import datetime
from datetime import timedelta
from configparser import ConfigParser

start_time = datetime.utcnow()
configfile = "bot.ini"
config =  ConfigParser()
config.read(configfile)

class Core(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def shutdown(self, ctx):
        if str(ctx.message.author.id) == str(config['other']['owner_id']):
            await ctx.reply("Shutting down...")
            print("Shutting down...")
            await self.bot.close()
        else:
            await ctx.reply("To shutdown bot, please contact owner.")
            print(str(ctx.message.author) + " has tried to shut down the bot.")

    @commands.command(pass_context=True)
    async def uptime(self,ctx):
        now = datetime.utcnow()
        delta = now - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
        uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
        await ctx.reply("Bot uptime: " + uptime_stamp)

async def setup(bot):
    await bot.add_cog(Core(bot))