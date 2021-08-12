import traceback
import sys
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound
from modules.functions import printt as print
from colorama import Fore

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )

        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.author.mention}, {ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send('I could not find that member. Please try again.')
        else:
            print(f'{Fore.RED}Ignoring exception in command {Fore.LIGHTBLUE_EX}{ctx.command}{Fore.LIGHTYELLOW_EX}: {Fore.LIGHTGREEN_EX}{type(error)}')
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            return await ctx.send(error)

def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))