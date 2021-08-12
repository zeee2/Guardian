from discord.ext import commands
import discord
from modules.functions import *
from modules.config import config

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def _help(self, ctx: commands.Context, *input):
        prefix = config["BotPrefix"]
        owner = config["ownerID"]

        if not input:
            owner = self.bot.get_user(owner)
            embed = discord.Embed(title="Guardian's Commands", color=converthex("65E3A6"))
            cog = []
            ignoreCogs = ["Jishaku", "Moderate", "ErrorHandler", "Help"]
            for i in self.bot.cogs:
                if i in ignoreCogs:
                    pass
                else:
                    cog.append(i)
            for cog in cog:
                for command in self.bot.get_cog(cog).get_commands():
                    # if cog is not hidden
                    if not ctx.message.author.guild_permissions.administrator or ctx.author.id != ctx.guild.owner_id:
                        if not command.name in ("customTitle", "customText", "role"):
                            if not command.hidden:
                                commands_help = command.help
                                if not commands_help == None:
                                    commands_help = command.help
                                else:
                                    commands_help = '***This command is under development!***'
                                embed.add_field(name=f"**{prefix}{command.name}**", value=commands_help, inline=True)
                    else:
                        if not command.hidden:
                            commands_help = command.help
                            if not commands_help == None:
                                commands_help = command.help
                            else:
                                commands_help = '***This command is under development!***'
                            embed.add_field(name=f"**{prefix}{command.name}**", value=commands_help, inline=True)
        else:
            embed = discord.Embed(title="Easter EGGGGGGGGGGGGGGGGGGGGGGGGG",
                                description="I don't know how you got here. But I didn't see this coming at all. :stuck_out_tongue_winking_eye:",
                                color=discord.Color.red())

        # setting information about author
        embed.add_field(name="About", value=f"Guardian is the discord bot that protect the server from bot spammers.\n\
                                        if this bot have some problem kinda bug, need to help, or have some idea, please contect to {owner.mention}.", inline=False)
            
        embed.set_footer(text="Guardian | Discord Server Guardian")

        return await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))