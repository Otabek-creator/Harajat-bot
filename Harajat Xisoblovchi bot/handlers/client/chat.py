from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import get_start
from states import MyStates, Kirim, Chiqim
from utils.database import users, kirim, chiqim
from loader import dp, bot


Help_Commands = f"""
/start - <b>botni ishga tushirish</b>
/help - <b>bot haqida malumot</b>
/kirim - <b>kirim qilish</b>
/chiqim - <b>chiqim qilish</b>
/result - <b>Kirim-Chiqim ma'lumotlari</b>
"""


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = users.get_user_by_id(message.from_user.id)

    if user is None:
        await message.answer("Ismingizni kiriting")
        await MyStates.ism.set()
    else:
        await bot.send_message(message.chat.id,
                               "Botdan foydalanishingiz mumkin😊",
                               reply_markup=await get_start())


@dp.message_handler(state=MyStates.ism)
async def ism(message: types.Message, state: FSMContext):
    await message.answer("Familyangizni kiriting")
    await state.update_data(ism=message.text)
    await MyStates.familya.set()


@dp.message_handler(state=MyStates.familya)
async def yosh(message: types.Message, state: FSMContext):
    await message.answer("Telefon nomeringizni kiriting")
    await state.update_data(familya=message.text)
    await MyStates.ph_number.set()


@dp.message_handler(state=MyStates.ph_number)
async def raqam(message: types.Message, state: FSMContext):
    await state.update_data(ph_number=message.text)
    data = await state.get_data()

    ism = data['ism']
    familya = data['familya']
    ph_number = data["ph_number"]
    chat_id = message.chat.id

    # Ma'lumotlarni bazaga saqlash
    users.create_user(ism, familya, ph_number, chat_id)

    await bot.send_message(message.chat.id,
                           "Botdan foydalanishingiz mumkin😊",
                           reply_markup= await get_start())

    await state.finish()


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(f'Bu yordamchi bot, menyudan kerakli bulimni tanlang \n {Help_Commands}',
                         parse_mode='HTML'
                         )


@dp.message_handler(commands=['kirim'])
async def k_ch_kiritish(message: types.Message):
    await message.answer("Kirimki kiriting")
    await Kirim.kirim.set()


@dp.message_handler(state=Kirim.kirim)
async def kirim_kiritish(message: types.Message, state: FSMContext):
    await message.answer("Kirim ma'lumotini kiriting")
    await state.update_data(kirim=message.text)
    await Kirim.sabab.set()


@dp.message_handler(state=Kirim.sabab)
async def sabob_kiritish(message: types.Message, state: FSMContext):
    await state.update_data(sabab=message.text)

    data = await state.get_data()

    krm = data["kirim"]
    sabab = data["sabab"]
    chat_id = message.chat.id

    kirim.add_user(krm, sabab, chat_id)

    await message.answer("Ma'lumotlaringiz saqlandi")

    await state.finish()


@dp.message_handler(commands=['chiqim'])
async def ch_k_kiritish(message: types.Message):
    await message.answer("Chiqim kiriting")
    await Chiqim.chiqim.set()


@dp.message_handler(state=Chiqim.chiqim)
async def chiqim_kiritish(message: types.Message, state: FSMContext):
    await message.answer("Chiqim ma'lumotini kiriting")
    await state.update_data(chiqim=message.text)
    await Chiqim.sabab.set()


@dp.message_handler(state=Chiqim.sabab)
async def sabab_kiritish(message: types.Message, state: FSMContext):
    await state.update_data(sabab=message.text)

    data = await state.get_data()

    chqm = data["chiqim"]
    sabab = data["sabab"]
    chat_id = message.chat.id

    chiqim.add_user(chqm, sabab, chat_id)

    await message.answer("Ma'lumotlaringiz saqlandi")

    await state.finish()


@dp.message_handler(commands=['result'])
async def natija(message: types.Message):
    malumot_kirim = kirim.get_user(message.chat.id)
    malumot_chiqim = chiqim.get_user(message.chat.id)
    result = ''
    total_kirim = 0
    total_chiqim = 0

    for user_kr in malumot_kirim:
        text_kr = f"Kirim: {user_kr[1]}\nSabab: {user_kr[2]}"
        total_kirim += user_kr[1]
        result += text_kr + '\n'

    for user_ch in malumot_chiqim:
        text_ch = f"Chiqim: {user_ch[1]}\nSabab: {user_ch[2]}"
        total_chiqim += user_ch[1]
        result += text_ch + '\n'

    qolgan = total_kirim - total_chiqim
    result += f"Jami Kirim: {total_kirim}\n"
    result += f"Jami Chiqim: {total_chiqim}\n"
    result += f"Qolgan Pul: {qolgan}\n"

    await message.answer(result)


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(text='menyudan foydalaning')
