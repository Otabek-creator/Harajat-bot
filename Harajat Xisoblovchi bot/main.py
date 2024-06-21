from loader import dp, bot, ADMIN
from handlers import *
from aiogram import executor, types


async def on_startup(dispatcher):
    await dispatcher.bot.set_my_commands(
                [
                    types.BotCommand('start', "Botni ishga tushirish"),
                    types.BotCommand('help', "Botdan foydalanish"),
                    types.BotCommand('kirim', "Kirim qilish"),
                    types.BotCommand('chiqim', "Chiqim qilish"),
                    types.BotCommand('result', "Kirim-Chiqim ma'lumotlari"),
                ]
    )

    await bot.send_message(chat_id=ADMIN, text="Bot ishga tushdi")


async def on_shutdown(dispatcher):
    await bot.send_message(chat_id=ADMIN, text="Bot To'xtadi")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
