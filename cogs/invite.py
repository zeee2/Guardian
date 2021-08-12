from discord.ext import commands
from discord import Embed
from modules.functions import *
import random

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite')
    async def _invite(self, ctx: commands.Context):
        """
        Shows invite links to bot.
        """
        embed = Embed(title="**here is my invite link!**", description="♥♥♥♥", colour=random.randint(0, 16777215))
        embed.set_footer(text=f"Guardian | Discord Server Guardian")
        fields = [("With Administrator Permissions", "https://discord.com/oauth2/authorize?client_id=852955874456764459&scope=bot&permissions=8", False),
                    ("With Minimal Permissions", "https://discord.com/oauth2/authorize?client_id=852955874456764459&scope=bot&permissions=2416307280", False),
                    ]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        return await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Invite(bot))