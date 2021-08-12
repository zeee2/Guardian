from colorama import Fore
from modules.functions import *
from modules.config import config
import pymysql

mysql_host = config["MysqlHost"]
mysql_user = config["MysqlId"]
mysql_password = config["MysqlPw"]
mysql_db = config["MysqlDb"]

def dberror():
    printt("{Fore.RED}An unknown problem has occurred.")
    cur.close()
    exit()

asciiArt()

printt("Connecting DB...")
try:
    conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8mb4')
except Exception as e:
    printt(f"{Fore.RED}DB Server Connect Failed")
    exit()
if conn != None:
    printt("Connecting!")
cur = conn.cursor()

printt("Create a new Database...")
try:
    cur.execute(f"CREATE DATABASE `Guardian`;")
    conn.commit()
except:
    dberror()
    
printt("Create a tables...")
try:
    cur.execute(f"""
        CREATE TABLE `auth_log` (
        `guild_id` bigint(20) NOT NULL,
        `guild_name` varchar(256) DEFAULT NULL,
        `userid` bigint(20) NOT NULL,
        `channel_id` bigint(20) NOT NULL,
        `time` timestamp NULL DEFAULT NULL,
        `is_verified` tinyint(1) DEFAULT NULL,
        `error_count` int(11) DEFAULT NULL,
        PRIMARY KEY (`userid`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    cur.execute(f"""
        CREATE TABLE `servers` (
        `guild_id` bigint(20) NOT NULL,
        `category_id` bigint(20) DEFAULT NULL,
        `customTitle` varchar(256) DEFAULT NULL,
        `customText` varchar(256) DEFAULT NULL,
        `noticeChannel` bigint(20) DEFAULT NULL,
        `verify_role` varchar(100) DEFAULT NULL,
        PRIMARY KEY (`guild_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    conn.commit()
except:
    dberror()

printt("ok, DB setup is complete!")