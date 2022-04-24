from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from utils.medapi import api
from loader import dp
from models.models import BodyLocations, Symptoms, TextModel, UserModel
from keyboards.inline.keyboards import language_keyboard
from keyboards.inline.med_keyboards import new_calculation_keyboard, change_settings_keyboards


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await UserModel.get_or_none(tg_id=message.chat.id)
    start_text = await TextModel.get(id=1)
    if not user:
        language = message.from_user.language_code
        user = await UserModel.create(tg_id=message.chat.id,
                                username=message.chat.username,
                                first_name=message.chat.first_name,
                                last_name=message.chat.last_name, 
                                language=language)

        await message.answer(start_text.ru_text, reply_markup=await change_settings_keyboards(language))
        language_text = await TextModel.get(id=2)
        language_text = language_text.ru_text if user.language else language_text.eng_text
        await message.answer(language_text, reply_markup=await language_keyboard())
    else:
        await message.answer(start_text.ru_text, reply_markup=await new_calculation_keyboard(user.language, 'back_general_location:'))
        

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    user = await UserModel.get(tg_id=message.chat.id)
    text = await TextModel.get(id=21)
    text = text.ru_text if user.language == 'ru' else text.eng_text
    await message.answer(text)
    