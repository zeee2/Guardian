from colorama import Fore 
import os
import datetime

def converthex(colorHex):
    try:
        colorHex = colorHex.replace("#", "")
    except:
        colorHex = colorHex
    convert = int(colorHex, 16)
    final = int(hex(convert), 0)
    return final
    
def asciiArt():
    print(f"{Fore.BLUE} ________  ___  ___  ________  ________  ________  ___  ________  ________      ")
    print(f"{Fore.BLUE}|\   ____\|\  \|\  \|\   __  \|\   __  \|\   ___ \|\  \|\   __  \|\   ___  \    ")
    print(f"{Fore.BLUE}\ \  \___|\ \  \\\\  \ \  \|\  \ \  \|\  \ \  \_|\ \ \  \ \  \|\  \ \  \\\ \  \   ")
    print(f"{Fore.BLUE} \ \  \  __\ \  \\\\  \ \   __  \ \   _  _\ \  \ \\\ \ \  \ \   __  \ \  \\\ \  \  ")
    print(f"{Fore.BLUE}  \ \  \|\  \ \  \\\\  \ \  \ \  \ \  \\\  \\\ \  \_\\\ \ \  \ \  \ \  \ \  \\\ \  \ ")
    print(f"{Fore.BLUE}   \ \_______\ \_______\ \__\ \__\ \__\\\ _\\\ \_______\ \__\ \__\ \__\ \__\\\\ \__\\")
    print(f"{Fore.BLUE}    \|_______|\|_______|\|__|\|__|\|__|\|__|\|_______|\|__|\|__|\|__|\|__| \|__|")
    print(f"")

def getNowtime():
    now = datetime.datetime.now()
    result = now.strftime("%Y-%m-%d %H:%M:%S")
    return result

def printt(contents):
    nowtime = getNowtime()
    print(f"{Fore.LIGHTGREEN_EX}{nowtime} | {Fore.LIGHTYELLOW_EX}{contents}{Fore.RESET}")

def loadAll_cogs(bot):
    printt(f"{Fore.LIGHTYELLOW_EX}Cogs {Fore.LIGHTBLUE_EX}jishaku {Fore.LIGHTYELLOW_EX}loding...")
    bot.load_extension(f'jishaku')
    printt(f"{Fore.LIGHTYELLOW_EX}Cogs {Fore.LIGHTBLUE_EX}jishaku {Fore.LIGHTYELLOW_EX}is successfully loaded")
    for cogs in os.listdir('./cogs'):
        if cogs.endswith('.py'):
            printt(f"{Fore.LIGHTYELLOW_EX}Cogs {Fore.LIGHTBLUE_EX}{cogs[:-3]} {Fore.LIGHTYELLOW_EX}loding...")
            bot.load_extension(f'cogs.{cogs[:-3]}')
            printt(f"{Fore.LIGHTYELLOW_EX}Cogs {Fore.LIGHTBLUE_EX}{cogs[:-3]} {Fore.LIGHTYELLOW_EX}is successfully loaded")