import discord
from discord.ext import commands
import requests
import praw
from configparser import ConfigParser
import asyncio

configfile = "./cogs/reddit.ini"
config =  ConfigParser()
config.read(configfile)

u=str(config['reddit']['username'])
p=str(config['reddit']['password'])
i=str(config['reddit']['client_id'])
s=str(config['reddit']['client_secret'])
a=str(config['reddit']['user_agent'])

reddit = praw.Reddit(username=u,password=p,client_id=i,client_secret=s,user_agent=a)


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search_reddit(self,ctx,subreddit_name:str,post_cnt:int,sort:str):
        subreddit = reddit.subreddit(subreddit_name)
        embed =  discord.Embed (title="r/"+str(subreddit_name))
        embed.set_footer(text="Data collected using PRAW by WOOT#4157")
        if str(sort)=="top":
            for submission in subreddit.top(limit=post_cnt):
                embed.add_field(name = "Title", value= str(submission.title))
                embed.add_field(name = "Upvotes", value= str(submission.score))
                embed.add_field(name = "ID", value= str(submission.id))
        elif str(sort) == "hot":
            for submission in subreddit.hot(limit=post_cnt):
                embed.add_field(name = "Title", value= str(submission.title))
                embed.add_field(name = "Upvotes", value= str(submission.score))
                embed.add_field(name = "ID", value= str(submission.id))
        elif str(sort) == "new":
            for submission in subreddit.new(limit=post_cnt):
                embed.add_field(name = "Title", value= str(submission.title))
                embed.add_field(name = "Upvotes", value= str(submission.score))
                embed.add_field(name = "ID", value= str(submission.id))
        await ctx.reply(embed=embed)

    @commands.command()
    async def content_reddit(self,ctx,id:str):
        submission = reddit.submission(id)
        embed = discord.Embed (title = str(submission.title) + " by u/" + str(submission.author.name) + " in r/" + str(submission.subreddit.name), description = str(submission.selftext))
        embed.add_field(name="Upvotes", value=str(submission.score))
        embed.add_field(name="Comments", value=str(submission.num_comments))
        embed.add_field(name="NSFW?", value=str(submission.over_18))
        embed.add_field(name="Locked?", value=str(submission.locked))
        embed.add_field(name="Spoiler?", value=str(submission.spoiler))
        embed.add_field(name="Link", value=str(submission.permalink))
        embed.set_footer(text="Data collected using PRAW by WOOT#4157")
        await ctx.reply(embed=embed)

    @commands.command()
    async def user_reddit(self, ctx, name: str):
        embed = discord.Embed(title="u/"+name)
        user = reddit.redditor(name)
        embed.add_field(name="Has gold?", value=str(user.is_gold))
        embed.add_field(name="Is mod?", value=str(user.is_mod))
        embed.add_field(name="Is employee?", value=str(user.is_employee))
        embed.add_field(name="Has verified email?", value=str(user.has_verified_email))
        embed.add_field(name="Comment karma", value=str(user.comment_karma))
        embed.add_field(name="Post karma", value=str(user.link_karma))
        embed.set_thumbnail(url=user.icon_img)
        await ctx.reply(embed=embed)

    @commands.command()
    async def subreddit_details(self,ctx,name:str):
        embed = discord.Embed(title="r/"+name)
        sub = reddit.subreddit(name)
        embed.add_field(name = "Description", value= sub.description)
        embed.add_field(name = "Is NSFW?", value = sub.over18)
        embed.add_field(name = "Members", value = sub.subscribers)
        await ctx.reply(embed=embed)





async def setup(bot):
    await bot.add_cog(Reddit(bot))