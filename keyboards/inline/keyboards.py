from aiogram import types


async def language_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="English", callback_data="language:en"))
    keyboard.add(types.InlineKeyboardButton(text="Русский", callback_data="language:ru"))
    return keyboard



async def change_profile_user(language):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Изменить пол и возраст" if language == 'ru' else 'Change gender and age', 
                                            callback_data="langauge:en"))
    keyboard.add(types.InlineKeyboardButton(text="Изменить язык" if language == 'ru' else 'Change language', 
                                            callback_data="langauge:ru"))
    return keyboard


async def change_gender_keyboard(language):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Мужчина" if language == 'ru' else 'Male', 
                                            callback_data="gender:male"))
    keyboard.add(types.InlineKeyboardButton(text="Женщина" if language == 'ru' else 'Female', 
                                            callback_data="gender:female"))
    return keyboard