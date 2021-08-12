import json
from os import path
from colorama import init, Fore
from modules.functions import *

init()
DefaultConfig = {
    "BotToken": "CHANGE THIS",
    "BotPrefix": ";",
    "ownerID": 637921223312932895,
    "MysqlHost": "CHANGE THIS",
    "MysqlId": "CHANGE THIS",
    "MysqlPw": "CHANGE THIS",
    "MysqlDb": "Guardian",
}

class JsonFile:
    @classmethod
    def saveDict(self, Dict, File="config.json"):
        #Saves a dict as a file
        with open(File, 'w') as json_file:
            json.dump(Dict, json_file, indent=4)

    @classmethod
    def GetDict(self, File="config.json"):
        #Returns a dict from file name
        if not path.exists(File):
            return {}
        else:
            with open(File) as f:
                data = json.load(f)
            return data
    
config = JsonFile.GetDict("./config.json")
Path = "./config.json"

#Config Checks
if config == {}:
    printt(f"{Fore.RED}Config Not Found.")
    printt(f"{Fore.YELLOW}Defalut config generating...")
    JsonFile.saveDict(DefaultConfig, Path)
    printt(f"{Fore.YELLOW}Config created! It is named 'config.json'. Edit it accordingly and start Guardian again!")
    exit()
else:
    #config check and updater
    AllGood = True
    NeedSet = []
    for key in list(DefaultConfig.keys()):
        if key not in list(config.keys()):
            AllGood = False
            NeedSet.append(key)

    if AllGood:
        printt(f"{Fore.BLUE}Configuration loaded successfully!")
    else:
        #fixes config
        printt(f"{Fore.BLUE}Updating config...")
        for key in NeedSet:
            config[key] = DefaultConfig[key]
            printt(f"{Fore.BLUE}Option {Fore.LIGHTYELLOW_EX}'{key}' {Fore.BLUE}added to config. Set default to {Fore.LIGHTYELLOW_EX}'{DefaultConfig[key]}'.")
        printt(f"{Fore.BLUE}Config updated! Please edit the new values to your liking.")
        JsonFile.saveDict(config, Path)
        exit()
