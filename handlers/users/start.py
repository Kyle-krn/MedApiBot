from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.medapi import api
from loader import dp
from models.models import BodyLocations, Symptoms, TextModel, UserModel
from keyboards.inline.keyboards import language_keyboard


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await UserModel.get_or_none(tg_id=message.chat.id)
    start_text = await TextModel.get(id=1)
    if not user:
        await  UserModel.create(tg_id=message.chat.id,
                                username=message.chat.username,
                                first_name=message.chat.first_name,
                                last_name=message.chat.last_name)
    await message.answer(start_text.ru_text)
    language_text = await TextModel.get(id=2)
    await message.answer(language_text.ru_text, reply_markup=await language_keyboard())
    # else:
    #     await message.answer(start_text.ru_text)
        


