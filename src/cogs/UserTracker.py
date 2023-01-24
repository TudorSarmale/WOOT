import discord
from discord.ext import commands
from discord import Member
from discord import Spotify
import asyncio
from configparser import ConfigParser
from datetime import datetime
import mysql.connector
import string
import calendar

configfile = "bot.ini"
config =  ConfigParser()
config.read(configfile)

class DBConnection(object):

    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME):
        self.host = DB_HOST
        self.port = DB_PORT
        self.name = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.con = None

    def connect_db(self):
        if self.con is None:
            self.con = mysql.connector.connect(host = self.host,
                                        port = self.port,
                                        db = self.name,
                                        user = self.user,
                                        passwd = self.password)
        return self.con

    def fetch_db(self, query):
        self.query = query
        self.cursor = self.con.cursor()
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()

        return self.result

    def insert_db(self, query):
        self.query = query
        self.cursor = self.con.cursor()
        self.cursor.execute(self.query)
        self.con.commit()

        return

class UserTracker(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    

    @commands.Cog.listener()
    async def on_member_update(self,before, after):
        user = self.bot.get_user(int(config['other']['owner_id']))
        if before.nick != after.nick:
            embed = discord.Embed(title=str(after.name) + "#" + str(after.discriminator) + " nickname change")
            embed.add_field(name="Old nickname", value=before.nick)
            embed.add_field(name="New nickname", value=after.nick)
            #await user.send("**Nickname change:**"+str(after.name)+"#"+str(after.discriminator) + " " + str(before.nick) + " :arrow_right: " + str(after.nick))
            await user.send(embed=embed)
        elif before.roles != after.roles:
            await user.send(str(after.name)+"#"+str(after.discriminator) + " " + str(before.roles) + " :arrow_right: " + str(after.roles))
        elif before.pending != after.pending:
            await user.send(str(after.name)+"#"+str(after.discriminator) + " " + str(before.pending) + " :arrow_right: " + str(after.pending))

    @commands.Cog.listener()
    async def on_user_update(self,before,after):
        user = self.bot.get_user(int(config['other']['owner_id']))
        if before.avatar != after.avatar:
            await user.send(str(after.name)+"#"+str(after.discriminator) + " **changed avatars!**")
        elif before.username != after.username:
            await user.send(str(after.name)+"#"+str(after.discriminator) + " " + str(before.name) + " :arrow_right: " + str(after.name))
        else:
            await user.send(str(after.name)+"#"+str(after.discriminator) + " " + str(before.discriminator) + " :arrow_right: " + str(after.discriminator))

    @commands.Cog.listener()
    async def on_presence_update(self,before,after):
        user = self.bot.get_user(int(config['other']['owner_id']))
        if before.status != after.status:
            embed = discord.Embed(title=str(after.name) + "#" + str(after.discriminator) + " presence change")
            embed.add_field(name="Old presence",value=str(before.status))
            embed.add_field(name="New presence", value=str(after.status))
            await user.send(embed=embed)

            
                
            


        elif after.activity != before.activity:
            embed = discord.Embed(title=str(after.name) + "#" + str(after.discriminator) + " activity change")
            embed.add_field(name="Old activity",value=str(before.activity))
            embed.add_field(name="New activity", value=str(after.activity))
            user = self.bot.get_user(int(config['other']['owner_id']))
            await user.send(embed=embed)

            date = datetime.utcnow()
            utc_time = calendar.timegm(date.utctimetuple())

            if str(after.activity) == "Spotify":
                if str(after.id) == str(901549090196824104):
                    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=str(after.activity.title)))

                embed2 = discord.Embed(title = f"{after.name}'s Spotify",description = "Listening to {}".format(after.activity.title),color = 0xC902FF)
                embed2.set_thumbnail(url=after.activity.album_cover_url)
                embed2.add_field(name="Artist", value=after.activity.artist)
                embed2.add_field(name="Album", value=after.activity.album)
                embed2.set_footer(text="Song started at {}".format(after.activity.created_at.strftime("%H:%M")))
                await user.send(embed=embed2)
                
            if str(after.id) == str(901549090196824104) and str(after.activity) == "None":
                    await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='you'))



    @commands.command() 
    async def status(self,ctx,member:discord.Member):
        await ctx.reply(member.raw_status)

    @commands.command()
    async def spotify(self,ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
            pass
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(title = f"{user.name}'s Spotify",description = "Listening to {}".format(activity.title),color = 0xC902FF)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.set_footer(text="Song started at {}".format(activity.created_at.strftime("%H:%M")))
                    await ctx.reply(embed=embed)
                    
    @commands.command()
    async def userinfo(self,ctx,usor:int,member: discord.Member):
        user = self.bot.get_user(int(usor))
        embed = discord.Embed(title = f"{user.name}#{user.discriminator}'s Data",description = "Data gathered by Vadim Bot#1840.",color = 0xC902FF)
        #embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="User ID", value=str(user.id))
        embed.add_field(name="Bot status", value=str(user.bot))
        embed.add_field(name="Created at", value=str(user.created_at))
        embed.add_field(name="Nickname (if none, then username)", value=str(user.display_name))
        if str(member.premium_since) != "None":
            embed.add_field(name="Nitro status", value="Active")
            embed.add_field(name="Nitro since", value=str(member.premium_since))
        else:
            embed.add_field(name="Nitro status", value="Inactive")
        embed.add_field(name="Status", value=str(member.status))
        embed.add_field(name="Desktop status", value=str(member.desktop_status))
        embed.add_field(name="Mobile status", value=str(member.mobile_status))
        embed.add_field(name="Web status", value=str(member.web_status))
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(UserTracker(bot))
    
