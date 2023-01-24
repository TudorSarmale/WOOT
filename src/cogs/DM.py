import discord
from discord.ext import commands
import asyncio
from configparser import ConfigParser

configfile = "bot.ini"
config =  ConfigParser()
config.read(configfile)


class DM(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command() 
    async def dm(self,ctx,usor:int,*args):
        if str(ctx.message.author.id) == str(config['other']['owner_id']):
            embed=discord.Embed(title="Use $contact to contact owner back.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description=str(' '.join(args)), color=discord.Color.blue())
            embed.set_author(name="Message from owner's bot.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", icon_url=str(config['bot']['avatar_url']))
            user = self.bot.get_user(int(usor))
            await user.send(embed=embed)
            await ctx.reply(f"{user.name}#{user.discriminator} messaged.")
        else:
            print(str(ctx.message.author) + " has tried to send a DM to somebody.")
            await ctx.reply("You do not have permissions to DM people. Only owner has rights to DM people.")

    @commands.command()
    async def contact(self,ctx,*args):
        user = self.bot.get_user(int(config['other']['owner_id']))
        embed=discord.Embed(title="You have been contacted.", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", description=str(' '.join(args)), color=discord.Color.blue())
        embed.set_author(name="Reply from " + str(ctx.message.author), url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", icon_url=ctx.message.author.avatar_url)
        await user.send(embed=embed)
        await ctx.reply("Owner contacted.")

async def setup(bot):
    await bot.add_cog(DM(bot))