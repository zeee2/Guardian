from discord.ext import commands
from modules.functions import *
from modules.config import config
from discord.utils import get
import pymysql


mysql_host = config["MysqlHost"]
mysql_user = config["MysqlId"]
mysql_password = config["MysqlPw"]
mysql_db = config["MysqlDb"]
Echeck = '\N{WHITE HEAVY CHECK MARK}'
Erobot = '\N{Robot Face}'
Ereload = '\N{Anticlockwise Downwards and Upwards Open Circle Arrows}'

class Unauth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unauth")
    async def _unauth(self, ctx: commands.Context):
        try:
            conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8mb4')
        except Exception as e:
            printt(f"{Fore.RED}DB Server Connect Failed")
            exit()
        cur = conn.cursor()

        guild = self.bot.get_guild(ctx.guild.id)
        guildID = ctx.guild.id
        guildName = ctx.guild.name
        UserID = ctx.author.id
        UserName = ctx.author
        member = ctx.author
        await ctx.message.delete()

        cur.execute(f'SELECT verify_role From servers WHERE guild_id={guildID}')
        ServerData = cur.fetchone()
        roleName = ServerData[0]
        role = get(member.guild.roles, name=roleName)
        await UserName.remove_roles(role)


def setup(bot: commands.Bot):
    bot.add_cog(Unauth(bot))