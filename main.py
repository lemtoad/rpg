# main bot file
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.load_extension("rpgcommands")

TOKEN = 'addtokenhere'

if __name__ == "__main__":
    asyncio.run(bot.start(TOKEN))
