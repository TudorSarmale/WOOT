import discord
from discord.ext import commands
import asyncio

class Example(commands.Cog):

	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def test(self,ctx):
		await ctx.reply("Test")

async def setup(bot):
	await bot.add_cog(Example(bot))