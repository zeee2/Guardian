from json import load
import discord
from discord.ext import commands
from discord import Embed
from modules.functions import *
import random
from colorama import Fore

class Moderate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cogs')
    async def _cogsMod(self, ctx: commands.Context, loadType=None, cogsName=None):
        def convertLoadType(loadType):
            if loadType == "load" or loadType == "l" or loadType == "lo":
                return "loaded"
            elif loadType == "unload" or loadType == "u" or loadType == "un":
                return "unloaded"
            elif loadType == "reload" or loadType == "r" or loadType == "re":
                return "reloaded"

        if ctx.author.id != 637921223312932895:
            return await ctx.message.add_reaction('❌')
        else:
            await ctx.message.add_reaction('✔️')

        cogs = []
        for i in self.bot.extensions.keys():
            cogs.append(i)
            
        async with ctx.typing():
            if loadType == None and cogsName == None:
                embed = Embed(title="Guardian's Cogs List", description="load, unload, reload is support", colour=random.randint(0, 16777215))
                embed.set_footer(text=f"Guardian | Discord Server Guardian")
                fields = []
                num = 0
                for i in cogs:
                    fields.append([f"Cogs #{num}", f"**{i}**", True])
                    num += 1
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                return await ctx.send(embed=embed)
            else:
                msg = await ctx.send("Please wait...")
                if not cogsName in "cogs.":
                    cogsName = f"cogs.{cogsName}"
                if cogsName == "*":
                    msgs = ""
                    if loadType == "load" or loadType == "l" or loadType == "lo":
                        for i in cogs:
                            self.bot.load_extension(i)
                            LoadType = convertLoadType(loadType)
                            msgs += f"Cogs **{i}** is successfully {LoadType}.\n"
                            await msg.edit(content=msgs)
                    elif loadType == "unload" or loadType == "u" or loadType == "un":
                        for i in cogs:
                            self.bot.unload_extension(i)
                            LoadType = convertLoadType(loadType)
                            msgs += f"Cogs **{i}** is successfully {LoadType}.\n"
                            await msg.edit(content=msgs)
                    elif loadType == "reload" or loadType == "r" or loadType == "re":
                        for i in cogs:
                            self.bot.reload_extension(i)
                            LoadType = convertLoadType(loadType)
                            msgs += f"Cogs **{i}** is successfully {LoadType}.\n"
                            await msg.edit(content=msgs)
                    else:
                        return await msg.edit(content = "command error!")
                    msgs += f"{LoadType} done."
                    await msg.edit(content=msgs)
                else:
                    if loadType == "load" or loadType == "l" or loadType == "lo":
                        self.bot.load_extension(cogsName)
                    elif loadType == "unload" or loadType == "u" or loadType == "un":
                        self.bot.unload_extension(cogsName)
                    elif loadType == "reload" or loadType == "r" or loadType == "re":
                        self.bot.reload_extension(cogsName)
                    else:
                        return await msg.edit(content = "command error!")
                    LoadType = convertLoadType(loadType)
                    printt(f"{Fore.LIGHTYELLOW_EX}Cogs {Fore.LIGHTBLUE_EX}{cogsName} {Fore.LIGHTYELLOW_EX}is {LoadType}.")
                    return await msg.edit(content=f"Cogs **{cogsName}** is successfully {LoadType}.")
                    

def setup(bot: commands.Bot):
    bot.add_cog(Moderate(bot))