
#  Guardian

Protect discord server from Bot Spammer!

## Setup
I will not help install mysql, but just prepare run guardian bot.

First, install the requirements.
```
$ python3 -m pip install -r requirements.txt
```
Once that's finished, you can go ahead and make a config file, by doing:
```
$ python3 run.py
$ nano config.json
```
Then you can go ahead and change the needed stuff in there. _MARKED WITH "CHANGE THIS"_

Once that's finished, you can go ahead and setup db tables, by doing:
```
$ python3 dbsetup.py
```

And the last thing you have to do, is running the Guardian Bot.
```
$ python3 run.py
```
If there's any issues during setup, feel free to post an issue.



## Requirements

- Experience developing in Python.
- Mysql Server (i use MariaDB)

  

## Example

[My Discord Server](https://discord.nerina.moe)



[Invite Gurdian Bot With Minimal Permissions](https://discord.com/oauth2/authorize?client_id=852955874456764459&scope=bot&permissions=2416307280)



[Invite Gurdian Bot With Administrator Permission](https://discord.com/oauth2/authorize?client_id=852955874456764459&scope=bot&permissions=8)
  

##  LICENSE

This project is licensed under the [GNU General Public License v3 (GPL-3)](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)). 
Please see [the license file](LICENSE) for more information.
