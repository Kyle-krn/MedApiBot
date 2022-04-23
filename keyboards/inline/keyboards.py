from aiogram import types
from models.models import TextButtonModel

async def language_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="English", callback_data="language:en"))
    keyboard.add(types.InlineKeyboardButton(text="Русский", callback_data="language:ru"))
    return keyboard



async def change_profile_user(language):
    keyboard = types.InlineKeyboardMarkup()
    btn1_text = await TextButtonModel.get(id=1)
    btn2_text = await TextButtonModel.get(id=2)
    keyboard.add(types.InlineKeyboardButton(text=btn1_text.ru_text if language == 'ru' else btn1_text.eng_text, 
                                            callback_data="langauge:en"))
    keyboard.add(types.InlineKeyboardButton(text=btn2_text.ru_text if language == 'ru' else btn2_text.eng_text, 
                                            callback_data="langauge:ru"))
    return keyboard


async def change_gender_keyboard(language):
    keyboard = types.InlineKeyboardMarkup()
    btn1_text = await TextButtonModel.get(id=3)
    btn2_text = await TextButtonModel.get(id=4)
    keyboard.add(types.InlineKeyboardButton(text=btn1_text.ru_text if language == 'ru' else btn1_text.eng_text, 
                                            callback_data="gender:male"))
    keyboard.add(types.InlineKeyboardButton(text=btn2_text.ru_text if language == 'ru' else btn2_text.eng_text, 
                                            callback_data="gender:female"))
    return keyboard



async def payments_keyboard(language: str):
    keyboard = types.InlineKeyboardMarkup()
    amount = 9900
    btn_text = await TextButtonModel.get(id=12)
    btn_text = btn_text.ru_text if language == 'ru' else btn_text.eng_text
    btn_text = btn_text.format(int(amount/100))
    btn1_text = await TextButtonModel.get(id=5)
    btn1_text = btn1_text.ru_text if language == 'ru' else btn1_text.eng_text
    keyboard.add(types.InlineKeyboardButton(text=btn_text, pay=True))
    keyboard.add(types.InlineKeyboardButton(text=btn1_text, callback_data="back_payments:"))
    return keyboard