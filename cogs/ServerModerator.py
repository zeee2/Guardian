from discord.ext import commands
from modules.functions import *
from modules.config import config

import discord
import pymysql


mysql_host = config["MysqlHost"]
mysql_user = config["MysqlId"]
mysql_password = config["MysqlPw"]
mysql_db = config["MysqlDb"]
Echeck = '\N{WHITE HEAVY CHECK MARK}'

class ServerModerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='customTitle')
    async def _setTitle(self, ctx: commands.Context, *, settings):
        """
            Set Custom Title.
        """
        if not ctx.message.author.guild_permissions.administrator or ctx.author.id != ctx.guild.owner_id:
            return await ctx.message.add_reaction('❌')
        else:
            await ctx.message.add_reaction('✔️')

            try:
                conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8mb4')
            except Exception as e:
                printt(f"{Fore.RED}DB Server Connect Failed")
                exit()
            cur = conn.cursor()

            #get Notice Channel
            cur.execute(f'SELECT noticeChannel From servers WHERE guild_id={ctx.guild.id}')
            channel = cur.fetchone()
            channel = channel[0]
            c = self.bot.get_channel(channel)
            async with ctx.typing():
                if settings in ';':
                    return await ctx.send('Custom title should not contain `;`.', delete_after=10)
                cur.execute(f'UPDATE servers SET customTitle="{settings}" WHERE guild_id={ctx.guild.id}')
                printt(f"{Fore.LIGHTGREEN_EX}{ctx.guild} {Fore.RESET}| {Fore.LIGHTYELLOW_EX}changed customTitle.")
                conn.commit()
                cur.close()
                embed = discord.Embed(title="Changed Settings", color=0xED4245)
                embed.add_field(name="custom Title has been changed successfully.",value=f"New customTitle: {settings}",inline=False)
                embed.set_footer(text="Guardian | Discord Server Guardian")
                await c.send(embed = embed)
                return await ctx.send('The custom title has been changed successfully.', delete_after=10)

    @commands.command(name='customText')
    async def _setText(self, ctx: commands.Context, *, settings):
        """
            Set Custom Text.
        """
        if not ctx.message.author.guild_permissions.administrator or ctx.author.id != ctx.guild.owner_id:
            return await ctx.message.add_reaction('❌')
        else:
            await ctx.message.add_reaction('✔️')

            try:
                conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8mb4')
            except Exception as e:
                printt(f"{Fore.RED}DB Server Connect Failed")
                exit()
            cur = conn.cursor()

            #get Notice Channel
            cur.execute(f'SELECT noticeChannel From servers WHERE guild_id={ctx.guild.id}')
            channel = cur.fetchone()
            channel = channel[0]
            c = self.bot.get_channel(channel)
            async with ctx.typing():
                if settings in ';':
                    return await ctx.send('Custom text should not contain `;`.', delete_after=10)
                cur.execute(f'UPDATE servers SET customText="{settings}" WHERE guild_id={ctx.guild.id}')
                printt(f"{Fore.LIGHTGREEN_EX}{ctx.guild} {Fore.RESET}| {Fore.LIGHTYELLOW_EX}changed customText.")
                conn.commit()
                cur.close()
                embed = discord.Embed(title="Changed Settings", color=0xED4245)
                embed.add_field(name="custom Text has been changed successfully.",value=f"New customText: {settings}",inline=False)
                embed.set_footer(text="Guardian | Discord Server Guardian")
                await c.send(embed = embed)
                return await ctx.send('The custom text has been changed successfully.', delete_after=10)

    @commands.command(name='role')
    async def _setRole(self, ctx: commands.Context, *, settings):
        """
            Set the roles to be give to users who successfully authenticate.
        """
        if not ctx.message.author.guild_permissions.administrator or ctx.author.id != ctx.guild.owner_id:
            return await ctx.message.add_reaction('❌')
        else:
            await ctx.message.add_reaction('✔️')

            try:
                conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8mb4')
            except Exception as e:
                printt(f"{Fore.RED}DB Server Connect Failed")
                exit()
            cur = conn.cursor()

            #get Notice Channel
            cur.execute(f'SELECT noticeChannel From servers WHERE guild_id={ctx.guild.id}')
            channel = cur.fetchone()
            channel = channel[0]
            c = self.bot.get_channel(channel)
            async with ctx.typing():
                if settings in ';':
                    return await ctx.send('Role should not contain `;`.', delete_after=10)
                cur.execute(f'UPDATE servers SET verify_role="{settings}" WHERE guild_id={ctx.guild.id}')
                printt(f"{Fore.LIGHTGREEN_EX}{ctx.guild} {Fore.RESET}| {Fore.LIGHTYELLOW_EX}changed Role.")
                conn.commit()
                cur.close()
                embed = discord.Embed(title="Changed Settings", color=0xED4245)
                embed.add_field(name="Role has been changed successfully.",value=f"New Role: {settings}",inline=False)
                embed.set_footer(text="Guardian | Discord Server Guardian")
                await c.send(embed = embed)
                return await ctx.send('Role has been changed successfully.', delete_after=10)



    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8mb4')
        except Exception as e:
            printt(f"{Fore.RED}DB Server Connect Failed")
            exit()
        cur = conn.cursor()

        guildName = str(guild.name)
        guildId = str(guild.id)
        guildOwnerId = str(guild.owner_id)
        guildOwnerName = str(guild.owner)
        guildOwner = self.bot.get_user(guildOwnerId)
        NoticeChannelName = "Guardian Notice"

        printt(f"{Fore.LIGHTBLUE_EX}{guildName}({guildId}){Fore.LIGHTYELLOW_EX} New Server Detect!")
        
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
            channel = discord.utils.get(guild.channels, name=NoticeChannelName)
        except:
            channel = await guild.create_text_channel(NoticeChannelName, category=category)
            channel_overwrite = discord.PermissionOverwrite()
            channel_overwrite.read_messages = False
            channel_overwrite.read_message_history = False
            channel_overwrite.send_messages = False
            await channel.set_permissions(guild.default_role, overwrite=channel_overwrite)
        if channel == None:
            channel = await guild.create_text_channel(NoticeChannelName, category=category)
            channel_overwrite = discord.PermissionOverwrite()
            channel_overwrite.read_messages = False
            channel_overwrite.read_message_history = False
            channel_overwrite.send_messages = False
            await channel.set_permissions(guild.default_role, overwrite=channel_overwrite)

        # #Todo: Create a Role named "Verified"
        # await guild.create_role(name="verified")
        # role = discord.utils.get(guild.roles, name="verified")

        # #set All channels Role
        # guild_channels = []
        # for guild in self.bot.guilds:
        #     for channel in guild.channels:
        #         overwrite = discord.PermissionOverwrite()
        #         overwrite.read_messages = True
        #         overwrite.read_message_history = True
        #         overwrite.send_messages = True
        #         overwrite.manage_channels = True
        #         await channel.set_permissions(guild.me, overwrite=overwrite)
        #         #set @everyone permissions
        #         channel_overwrite = discord.PermissionOverwrite()
        #         channel_overwrite.read_messages = False
        #         channel_overwrite.read_message_history = False
        #         channel_overwrite.send_messages = False
        #         await channel.set_permissions(guild.default_role, overwrite=channel_overwrite)
        #         #set Role permissions
        #         overwritee = discord.PermissionOverwrite()
        #         overwritee.read_messages = True
        #         overwritee.read_message_history = True
        #         overwritee.send_messages = True
        #         await channel.set_permissions(role, overwrite=overwritee)

        #commit the data
        cur.execute(f'INSERT INTO servers VALUES({guildId}, "{category.id}", "", "", {channel.id}, "verified") ON DUPLICATE KEY UPDATE guild_id={guildId}, category_id="{category.id}", customText="", noticeChannel={channel.id}, verify_role="verified"')
        conn.commit()
        cur.close()

        #make a discord embed
        embed = discord.Embed(title="Thank you for using the Guardian!", color=0x62c1cc)
        embed.add_field(name="Please don't delete and edit This channel!",value=f"User's captcha log, developer's announcement will be send on this channel! If you modify the name of this channel, the bot will not work smoothly, so please do not modify or delete this channel!",inline=False)
        embed.add_field(name="Where is the commands list?",value=f"please enter the command **{config['BotPrefix']}help** .",inline=False)
        embed.set_footer(text="Guardian | Discord Server Guardian")
        msg = await channel.send(embed = embed)


def setup(bot: commands.Bot):
    bot.add_cog(ServerModerator(bot))