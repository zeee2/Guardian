from discord.ext import commands
import discord
from colorama import Fore
from modules.functions import *
from modules.config import config

asciiArt()

token = config["BotToken"]
prefix = config["BotPrefix"]

game = discord.Game(f"Discord Server Guardian")
bot = commands.Bot(command_prefix=prefix,status=discord.Status.online,activity=game, intents=discord.Intents.all(), help_command=None)

loadAll_cogs(bot)

@bot.event
async def on_ready():
    print(f"{Fore.GREEN}Guardian {Fore.LIGHTMAGENTA_EX}is ready{Fore.RESET}")

bot.run(token)