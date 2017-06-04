import discord
from discord.ext import commands
from discord.embeds import Embed
from discord import Game
from cexapi import CexApi
import json
from urllib.parse import quote

description = '''A bot that integrates into the CEX website to allow easy CEX price lookups and stock estimations'''
bot = commands.Bot(command_prefix='?', description=description)
cexapi = CexApi()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    await bot.change_presence(game=Game(name='with Lewis\' feelings'))

@bot.command()
async def search(*, search : str):
    product = cexapi.searchFirstWithStock(search)

    if product == []:
        await bot.say('No results found!')
    else:
        productPage = cexapi.lookupProductPage(product['id'])

        embed = buildEmbed(product, productPage['image_url'])

        await bot.say(embed=embed)

@bot.event
async def on_message(message):
    if message.author is not bot.user.name: 
        for word in message.content.split():
            if word.startswith(cexapi.CEX_PRODUCT_PAGE.format('uk', '')):
                lookup = cexapi.cexScrape(word)
                if 'product' in lookup:
                    if len(lookup['product']) > 0:
                        embed = buildEmbed(lookup['product'], lookup['product']['image_url'])
                        await bot.send_message(message.channel, embed=embed)
                        return


    await bot.process_commands(message)

def buildEmbed(product, image_url):
    embed = Embed()
    embed.title = product['name']
    embed.url = cexapi.CEX_PRODUCT_PAGE.format('uk', product['id'])

    stock = int(product['stock'])
    if stock == 10:
        stock = "10+"

    embed.add_field(name='Category', value=product['category'], inline=False)
    embed.add_field(name='Stock', value=stock, inline=False)
    embed.add_field(name='Buy Price', value=product['unit_price'], inline=False)
    embed.add_field(name='Sell for Voucher', value=product['exchange_price'], inline=True)
    embed.add_field(name='Sell for Cash', value=product['cash_price'], inline=True)

    embed.set_thumbnail(url=cexapi.CEX_BASE.format(
        'uk', quote(image_url)))

    return embed


# CeXyBot
# Config stuff

with open('config.json', 'r') as configHandle:
    config = json.loads(configHandle.read())

bot.run(config['token'])