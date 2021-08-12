from discord.ext import commands
from modules.functions import *
from modules.config import config
from captcha.image import ImageCaptcha
from discord.utils import get

import requests
import random
import pymysql
import time
import string
import asyncio
import discord


mysql_host = config["MysqlHost"]
mysql_user = config["MysqlId"]
mysql_password = config["MysqlPw"]
mysql_db = config["MysqlDb"]
Echeck = '\N{WHITE HEAVY CHECK MARK}'
Erobot = '\N{Robot Face}'
Ereload = '\N{Anticlockwise Downwards and Upwards Open Circle Arrows}'

class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def welcomeText(self, guild, guildID, guildName, UserID, UserName, member):
        try:
            conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8mb4')
        except Exception as e:
            printt(f"{Fore.RED}DB Server Connect Failed")
            exit()
        cur = conn.cursor()

        channel_name = f"Auth_{UserID}"

        printt(f"{Fore.LIGHTBLUE_EX}{UserName}({UserID}){Fore.LIGHTYELLOW_EX} has join the server at {guildName}({guildID})")
        
        #Todo: Get Category
        try:
            category = discord.utils.get(guild.categories, name="Guardian")
        except: #if it has something wrong, Create a Auth Category
            printt(f'{Fore.RED}Guardian Category is not found at {guildName} so i will make a one.')
            category = await guild.create_category("Guardian")
        if category == None:
            printt(f'{Fore.RED}Guardian Category is not found at {guildName} so i will make a one.')
            category = await guild.create_category("Guardian")
        
        #Todo: Create a Channel And Set Permission
        try:
            channel = discord.utils.get(guild.channels, name=channel_name)
        except:
            channel = await guild.create_text_channel(channel_name, category=category)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.read_message_history = False
            overwrite.send_messages = True
            await channel.set_permissions(guild.me, overwrite=overwrite)
            await channel.set_permissions(member, overwrite=overwrite)
            channel_overwrite = discord.PermissionOverwrite()
            channel_overwrite.read_messages = False
            channel_overwrite.read_message_history = False
            channel_overwrite.send_messages = False
            await channel.set_permissions(guild.default_role, overwrite=channel_overwrite)
        if channel == None:
            channel = await guild.create_text_channel(channel_name, category=category)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            overwrite.read_message_history = True
            overwrite.send_messages = True
            await channel.set_permissions(guild.me, overwrite=overwrite)
            await channel.set_permissions(member, overwrite=overwrite)
            channel_overwrite = discord.PermissionOverwrite()
            channel_overwrite.read_messages = False
            channel_overwrite.read_message_history = False
            channel_overwrite.send_messages = False
            await channel.set_permissions(guild.default_role, overwrite=channel_overwrite)

        #commit the data
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(f'INSERT INTO auth_log VALUES({guildID}, "{guildName}", {UserID}, {channel.id}, "{timestamp}", 0, 0) ON DUPLICATE KEY UPDATE guild_id={guildID}, guild_name="{guildName}", userid={UserID}, channel_id={channel.id}, time="{timestamp}", is_verified=0, error_count=0')
        conn.commit()

        #send a captcha on private channel
        #create captcha image
        string_pool = string.ascii_letters + string.digits
        captcha = ""
        for i in range(6):
            captcha += random.choice(string_pool)
        Image_captcha = ImageCaptcha()
        name = f"./captcha/{UserID + guildID}.jpg"
        Image_captcha.write(captcha, name)

        #get customText
        cur.execute(f'SELECT customTitle, customText, noticeChannel, verify_role From servers WHERE guild_id={guildID}')
        ServerData = cur.fetchone()
        customTitle = ServerData[0]
        customText = ServerData[1]
        nc = self.bot.get_channel(ServerData[2])
        roleName = ServerData[3]

        #make a discord embed
        embed = discord.Embed(title=f"{Erobot} I'm ROBOT. You too? :BeepBeep:", color=0x62c1cc)
        if len(customText) > 0 and len(customTitle) > 0:
            embed.add_field(name=customTitle,value=customText,inline=False)
        embed.add_field(name="Why should I do this?",value=f"Because, before using the server, it is a necessary procedure to prove that you are a human, not a bot.",inline=False)
        embed.add_field(name="Where is my captcha code?",value=f"If you press the check reaction, the captcha code will appear.",inline=True)
        embed.set_footer(text="Guardian | Discord Server Guardian")
        msg = await channel.send(embed = embed)
        msg1 = await channel.send(member.mention)
        await msg1.delete()
        await msg.add_reaction(Echeck)
        def check(reaction, user):
            return str(reaction.emoji) == Echeck and not user.id == 852955874456764459 and reaction.message.id == msg.id
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add',check=check,timeout=None)
            except asyncio.TimeoutError:
                pass    
            else:
                if str(reaction.emoji) == Echeck and UserID == user.id:
                    await msg.clear_reactions()
                    await msg.delete()
                    return await self.renewCaptcha(member, channel, roleName, nc)
                            
                elif str(reaction.emoji) == Echeck and UserID != user.id:
                    await msg.remove_reaction(Echeck, user)

    async def renewCaptcha(self, member, channel, roleName ,nc):
        try:
            conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8mb4')
        except Exception as e:
            printt(f"{Fore.RED}DB Server Connect Failed")
            exit()
        cur = conn.cursor()

        guild = self.bot.get_guild(member.guild.id)
        guildID = member.guild.id
        guildName = member.guild.name
        UserID = member.id
        UserName = member
        channel_name = f"Auth_{UserID}"

        #renew captcha img
        string_pool = string.ascii_uppercase + string.digits
        captcha = ""
        for i in range(6):
            captcha += random.choice(string_pool)
        Image_captcha = ImageCaptcha()
        name = f"./captcha/{UserID + guildID}.jpg"
        Image_captcha.write(captcha, name)
        printt(f"{Fore.LIGHTBLUE_EX}{guildName}{Fore.LIGHTYELLOW_EX}|{Fore.LIGHTBLUE_EX}{UserName}({UserID}) {Fore.LIGHTYELLOW_EX}captcha code: {captcha}")

        #renew timestamp
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        img = await channel.send(file=discord.File(name))
        await img.edit(content="Please enter **RENEW** if you want to renew the captcha code.\nAll alphabets must be **uppercase letters**. 모든 알파뱃은 대문자 입니다.\nThe code should **not** contain any spaces. 공백없이 **붙여** 작성해주세요.")
        def check(msg):
            return msg.author == UserName and msg.channel == channel
        while True:         
            try:
                msg = await self.bot.wait_for("message", timeout=60, check=check)
            except:
                await channel.send("Time Out!", delete_after= 8)
                await img.delete()
                #delete channel
                await channel.delete()
                #add error count at db
                cur.execute(f'SELECT error_count From auth_log WHERE guild_id={guildID} and userid={UserID}')
                data = cur.fetchone()
                errCount = data[0]
                cur.execute(f'UPDATE auth_log SET error_count = {errCount + 1} WHERE guild_id={guildID} and userid={UserID}')
                conn.commit()
                cur.close()
                #send dm
                dmc = await member.create_dm()
                embed = discord.Embed(title="Authentication Failed", color=0xF23A3A)
                embed.add_field(name="Server with failed user authentication",value=guildName,inline=True)
                embed.add_field(name="User authentication failure time:",value=f"{timestamp} (KST)",inline=False)
                embed.set_footer(text="Guardian | Discord Server Guardian")     
                await dmc.send(embed = embed) 
                #user kick
                # await member.kick(reason="Authentication Failed | captcha timeout")
                #send notice channel
                embed = discord.Embed(title="User authentication failed", color=0xF23A3A)
                embed.add_field(name="User",value=f"{member.mention}",inline=False)
                embed.add_field(name="time",value=f"{timestamp} (KST)",inline=False)
                embed.set_footer(text="Guardian | Discord Server Guardian")
                msg = await nc.send(embed = embed)
                return
            if msg.content == captcha:
                await img.delete()
                await msg.delete()
                #give role
                role = get(member.guild.roles, name=roleName)
                await UserName.add_roles(role)
                #delete channel
                await channel.set_permissions(UserName, overwrite=None)
                await channel.delete()
                #update verify data
                cur.execute(f'UPDATE auth_log SET is_verified = 1 WHERE guild_id={guildID} and userid={UserID}')
                conn.commit()
                cur.close()
                #send dm
                dmc = await member.create_dm()
                embed = discord.Embed(title="Authentication Successful!", color=0x62c1cc)
                embed.add_field(name="server:",value=guildName,inline=True)
                embed.add_field(name="Role",value=roleName,inline=True)
                embed.add_field(name="Authorized time:",value=f"{timestamp} (KST)",inline=False)
                embed.set_footer(text="Guardian | Discord Server Guardian")     
                await dmc.send(embed = embed) 
                #send notice channel
                embed = discord.Embed(title="User authentication Successful", color=0x18F974)
                embed.add_field(name="User",value=f"{member.mention}",inline=False)
                embed.add_field(name="time",value=f"{timestamp} (KST)",inline=False)
                embed.set_footer(text="Guardian | Discord Server Guardian")
                msg = await nc.send(embed = embed)
                return
            elif msg.content == "renew" or msg.content == "RENEW":
                await msg.delete()
                await img.delete()
                return await self.renewCaptcha(member, channel, roleName, nc)
            else:
                await channel.send("The captcha code does not match.")  
                await msg.delete()
                #add error count at db
                cur.execute(f'SELECT error_count From auth_log WHERE guild_id={guildID} and userid={UserID}')
                data = cur.fetchone()
                errCount = data[0]
                cur.execute(f'UPDATE auth_log SET error_count = {errCount + 1} WHERE guild_id={guildID} and userid={UserID}')
                conn.commit()

    @commands.command(name="auth")
    async def _auth(self, ctx: commands.Context):
        """
            Create an authentication channel manually. 
        """
        guild = self.bot.get_guild(ctx.guild.id)
        guildID = ctx.guild.id
        guildName = ctx.guild.name
        UserID = ctx.author.id
        UserName = ctx.author
        member = ctx.author
        await ctx.message.delete()
        return await self.welcomeText(guild, guildID, guildName, UserID, UserName, member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(member.guild.id)
        guildID = member.guild.id
        guildName = member.guild.name
        UserID = member.id
        UserName = member
        return await self.welcomeText(guild, guildID, guildName, UserID, UserName, member)


def setup(bot: commands.Bot):
    bot.add_cog(Auth(bot))