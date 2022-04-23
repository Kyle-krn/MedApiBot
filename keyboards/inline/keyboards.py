from aiogram import types
from models.models import TextButtonModel

async def language_keyboard(first: bool = True):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="English", callback_data="language:en" if first else "set_language:en"))
    keyboard.add(types.InlineKeyboardButton(text="Русский", callback_data="language:ru" if first else "set_language:ru"))
    return keyboard



# async def change_profile_user(language):
    
    # return keyboard


async def change_gender_keyboard(language, first: bool = True):
    keyboard = types.InlineKeyboardMarkup()
    btn1_text = await TextButtonModel.get(id=3)
    btn2_text = await TextButtonModel.get(id=4)
    keyboard.add(types.InlineKeyboardButton(text=btn1_text.ru_text if language == 'ru' else btn1_text.eng_text, 
                                            callback_data="gender:male" if first else "set_gender:male"))
    keyboard.add(types.InlineKeyboardButton(text=btn2_text.ru_text if language == 'ru' else btn2_text.eng_text, 
                                            callback_data="gender:female" if first else "set_gender:female"))
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