import discord
from discord.ext import commands
import pprint
import json
from requests import Request, Session
import asyncio
from configparser import ConfigParser

configfile = "./cogs/cryptostuff.ini"
config =  ConfigParser()
config.read(configfile)

cmc_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

class CryptoStuff(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def crypto(self,ctx, symb:str, coin:str):
        parameters = {
            'symbol':symb,
            'convert':coin
        }

        headers = {
            'Accepts':'application/json',
            'X-CMC_PRO_API_KEY':str(config['cmc']['api_key'])
        }

        session = Session()
        session.headers.update(headers)
        response = session.get(cmc_url, params=parameters)
        #await ctx.reply(json.loads(response.text)['data'][symb]['quote'][coin]['price'])

        embed = discord.Embed(title = str(json.loads(response.text)['data'][symb]['name'] + " " + str(json.loads(response.text)['data'][symb]['symbol'])))
        if int(json.loads(response.text)['data'][symb]['is_active']) == 1:
            embed.add_field(name="Is active?", value = "Yes")
        else:
            embed.add_field(name="Is active?", value = "No")

        if int(json.loads(response.text)['data'][symb]['is_fiat']) == 1:
            embed.add_field(name="Is FIAT?", value = "Yes")
        else:
            embed.add_field(name="Is FIAT?", value = "No")

        embed.add_field(name="MAX supply", value= str(json.loads(response.text)['data'][symb]['max_supply']))
        embed.add_field(name="Market cap", value = str(json.loads(response.text)['data'][symb]['quote'][coin]['market_cap']))
        embed.add_field(name="Percent change 1h", value = str(json.loads(response.text)['data'][symb]['quote'][coin]['percent_change_1h']))
        embed.add_field(name="Percent change 24h", value = str(json.loads(response.text)['data'][symb]['quote'][coin]['percent_change_24h']))
        embed.add_field(name="Percent change 7d", value = str(json.loads(response.text)['data'][symb]['quote'][coin]['percent_change_7d']))
        embed.add_field(name="Percent change 30d", value = str(json.loads(response.text)['data'][symb]['quote'][coin]['percent_change_30d']))
        embed.add_field(name="Percent change 60d", value = str(json.loads(response.text)['data'][symb]['quote'][coin]['percent_change_60d']))
        embed.add_field(name="Percent change 90d", value = str(json.loads(response.text)['data'][symb]['quote'][coin]['percent_change_90d']))
        embed.add_field(name="Volume change 24h", value = str(json.loads(response.text)['data'][symb]['quote'][coin]['volume_change_24h']))
        embed.add_field(name="Volume 24h", value = str(json.loads(response.text)['data'][symb]['quote'][coin]['volume_24h'])) 
        embed.add_field(name="Price",value=str(json.loads(response.text)['data'][symb]['quote'][coin]['price']))
        embed.add_field(name="MAX supply", value= str(json.loads(response.text)['data'][symb]['total_supply']))
        embed.set_footer(text="Data collected from Coin Market Cap.")

        await ctx.reply(embed=embed)
        #pprint.pprint(json.loads(response.text))

async def setup(bot):
    await bot.add_cog(CryptoStuff(bot))