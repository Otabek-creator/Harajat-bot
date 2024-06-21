from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



async def get_start_admin():

      btn = ReplyKeyboardMarkup(resize_keyboard=True)
      btn.add(KeyboardButton('Salom')).insert(KeyboardButton("Send Post"))
      btn.add(KeyboardButton("Obunachilar ro'yxatini"))

      return btn