import asyncpg
import asyncio
import aiogram
import datetime
import random
import config
from config import DB
from sshtunnel import SSHTunnelForwarder

def sshserver():
    try:
        global server
        server = SSHTunnelForwarder(
        ('', 2222),
        ssh_username="",
        ssh_password="",
        remote_bind_address=('127.0.0.1', 5432)
        )
        server.start()
    except:
        print("ERROR: sshserver connection failed.")
        raise SystemExit(1)
        
async def main():
    try:
        global conn 
        conn = await asyncpg.connect(
            host=DB().HOST, 
            port=server.local_bind_port, 
            user=DB().USER().NAME, 
            password=DB().USER().PASSWORD, 
            database=DB().DATABASE
        )
        await conn.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = '{DB().DATABASE}';")
    except:
        print("ERROR: db connect failed.")
        raise SystemExit(2)

async def get_exp(message, user_id):
    try:
        return await conn.fetchval(f"SELECT exp FROM users WHERE user_id={user_id};")
    except Exception as e:
        await message.reply(f"Произошла ошибка\n```{e}```\nв функции get_exp\n__пожалуйста перешлите это сообщение @GipoGram для исправления ошибки.__")
async def add_exp(message, user_id, count):
    try:
        exp=await get_exp(message, user_id)
        await conn.execute(f"UPDATE users SET exp={int(exp)+int(count)} WHERE user_id={user_id};")
        return True
    except Exception as e:
        await message.reply(f"Произошла ошибка\n```{e}```\nв функции add_exp\n__пожалуйста перешлите это сообщение @GipoGram для исправления ошибки.__")
async def zero_exp(message, user_id):
    try:
        await conn.execute(f"UPDATE users SET exp=0 WHERE user_id={user_id};")
        return True
    except Exception as e:
        await message.reply(f"Произошла ошибка\n```{e}```\nв функции zero_exp\n__пожалуйста перешлите это сообщение @GipoGram для исправления ошибки.__")

async def get_barv(message, user_id):
    try:
        return await conn.fetchval(f"SELECT barv FROM users WHERE user_id={user_id};")
    except Exception as e:
        await message.reply(f"Произошла ошибка\n```{e}```\nв функции get_barv\n__пожалуйста перешлите это сообщение @GipoGram для исправления ошибки.__")
async def add_barv(message, user_id, count):
    try:
        barv=await get_barv(message, user_id)
        await conn.execute(f"UPDATE users SET barv={int(barv)+int(count)} WHERE user_id={user_id};")
        return True
    except Exception as e:
        await message.reply(f"Произошла ошибка\n```{e}```\nв функции add_barv\n__пожалуйста перешлите это сообщение @GipoGram для исправления ошибки.__")
async def zero_barv(message, user_id):
    try:
        await conn.execute(f"UPDATE users SET barv=0 WHERE user_id={user_id};")
        return True
    except Exception as e:
        await message.reply(f"Произошла ошибка\n```{e}```\nв функции zero_barv\n__пожалуйста перешлите это сообщение @GipoGram для исправления ошибки.__")

async def get_admin_lvl(message, user_id):
    try:
        return await conn.fetchval(f"SELECT admin_lvl FROM users WHERE user_id={user_id}")
    except Exception as e:
        await message.reply(f"Произошла ошибка\n```{e}```\nв функции get_admin_lvl\n__пожалуйста перешлите это сообщение @GipoGram для исправления ошибки.__")
async def set_admin_lvl(message, user_id, lvl):
    try:
        await conn.execute(f"UPDATE users SET admin_lvl={lvl} WHERE user_id={user_id};")
        return True
    except Exception as e:
        await message.reply(f"Произошла ошибка\n```{e}```\nв функции set_admin_lvl\n__пожалуйста перешлите это сообщение @GipoGram для исправления ошибки.__")

