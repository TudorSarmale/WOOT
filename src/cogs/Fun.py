import discord
from discord.ext import commands
import asyncio
import random

r = ["It is certain.",
     "It is decidedly so .",
     "Without a doubt .",
     "Yes definitely .",
     "You may rely on it .",

     "As I see it, yes .",
     "Most likely .",
     "Outlook good .",
     "Yes .",
     "Signs point to yes .",

     "Reply hazy, try again .",
     "Ask again later .",
     "Better not tell you now .",
     "Cannot predict now .",
     "Concentrate and ask again .",

     "Don't count on it .",
     "My reply is no .",
     "My sources say no .",
     "Outlook not so good .",
     "Very doubtful ."]


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ball(self, ctx, *args):
        await ctx.reply(r[random.randint(0, 25)])

    @commands.command()
    async def flip(self, ctx):
        embed = discord.Embed(title="Flip a Coin!")
        if (random.randint(0, 1) == 0):
            embed.set_thumbnail(url="https://i.ibb.co/MDcXrNM/head.png")
        else:
            embed.set_thumbnail(url="https://i.ibb.co/ccDq0v6/tails.png")
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
