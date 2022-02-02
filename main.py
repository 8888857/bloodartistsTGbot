from aiogram import Bot, Dispatcher, executor, types
import config
from config import TOKEN
import database as db

# Initialize bot and dispatcher
client_ = Bot(token=TOKEN)
client = Dispatcher(client_)

async def main():
    db.sshserver()
    await db.main()
    client_info = client_.get_me()
    print(f"{client_info.username} успешно запущен.")
    

@client.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ \"BloodArtists\" - бот созданый для ранговой и валютной системы чата \"🩸Кровавые Художники🩸\"\n\nбота создал @GipoGram", parse_mode="Markdown")
    
@client.message_handler(commands=["профиль", "profile"])
async def profile_(message: types.Message):
    exp=await db.get_exp(message, message.from_user.id)
    lvl=None
    barv=await db.get_barv(message, message.from_user.id)
    admin_lvl=await db.get_admin_lvl(message, message.from_user.id)
    if admin_lvl == 2:
        role="\nРоль: Админ"
    elif admin_lvl == 1:
        role="\nМодератор"
    else:
        role=None
    await message.reply(f"Профиль {message.from_user.username}\nУровень: {lvl}\nОпыт: {exp/10}\nБарвы🪙: {barv}{role}")
    
@client.message_handler()
async def on_message(message: types.Message):
    await 
    await db.add_exp(message, message.from_user.id, 1)
    
if __name__ == '__main__':
    executor.start_polling(client, skip_updates=True)