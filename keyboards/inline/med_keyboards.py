from aiogram import types
from models.models import BodyLocations, Symptoms, UserModel, TextButtonModel
from typing import List

async def choice_body_location(language: str):
    keyboard = types.InlineKeyboardMarkup()
    general_location = await BodyLocations.filter(parent_id__isnull=True)
    for item in general_location:
        keyboard.add(types.InlineKeyboardButton(text=item.ru_name if language == 'ru' else item.eng_name,
                                                callback_data=f"general_location:{item.id}"))
    return keyboard


async def choice_body_sublocation(language: str, sublocations: List[BodyLocations]):
    keyboard = types.InlineKeyboardMarkup()
    text = TextButtonModel.get(id=6)
    for item in sublocations:
        if len(await item.symptoms.all()) > 0:
            keyboard.add(types.InlineKeyboardButton(text=item.ru_name if language == 'ru' else item.eng_name,
                                                    callback_data=f"sublocation:1:{item.id}"))
    
    text = await TextButtonModel.get(id=6)
    text = text.ru_text if language == 'ru' else text.eng_text
    keyboard.add(types.InlineKeyboardButton(text=text,
                                            callback_data="back_general_location:"
                                            ))
    return keyboard


async def choice_symptoms_keyboard(user: UserModel, 
                                   symptoms: List[Symptoms], 
                                   page: int, 
                                   max_page: int, 
                                   sublocation_id: int):
    keyboard = types.InlineKeyboardMarkup()
    user_symptoms = await user.symptoms.all()
    for item in symptoms:
        text = item.ru_name if user.language == 'ru' else item.eng_name
        if item in user_symptoms:
            text = "✅ " + text
        keyboard.add(types.InlineKeyboardButton(text=text, 
                                                callback_data=f"add_symptom:{page}:{sublocation_id}:{item.id}"))

    prev_button = types.InlineKeyboardButton(text="⬅", callback_data=f"sublocation:{page-1}:{sublocation_id}")
    page_button = types.InlineKeyboardButton(text=f"{page}/{max_page} 📄", callback_data=f"empty_callback:")
    next_button = types.InlineKeyboardButton(text="➡", callback_data=f"sublocation:{page+1}:{sublocation_id}")
    prev = page - 1 > 0
    next = page + 1 <= max_page
    
    if prev and next:
        keyboard.add(prev_button, page_button, next_button)
    elif prev:
        keyboard.add(prev_button, page_button)
    elif next:
        keyboard.add(page_button, next_button)
    text = await TextButtonModel.get(id=7)
    text = text.ru_text if user.language == 'ru' else text.eng_text
    keyboard.add(types.InlineKeyboardButton(text=text, 
                                                callback_data=f"apply_symptom:"))
    return keyboard



async def symptoms_control_keyboard(language:str):
    keyboard = types.InlineKeyboardMarkup()
   
    btn_text = await TextButtonModel.get(id=8)
    btn_text = btn_text.ru_text if language == 'ru' else btn_text.eng_text
    keyboard.add(types.InlineKeyboardButton(text=btn_text, callback_data="find_diagnosis:"))
    
    btn1_text = await TextButtonModel.get(id=9)
    btn1_text = btn1_text.ru_text if language == 'ru' else btn1_text.eng_text
    keyboard.add(types.InlineKeyboardButton(text=btn1_text, callback_data="back_general_location:"))
    
    btn2_text = await TextButtonModel.get(id=10)
    btn2_text = btn2_text.ru_text if language == 'ru' else btn2_text.eng_text
    keyboard.add(types.InlineKeyboardButton(text=btn2_text, callback_data="clear_symptoms:"))

    # keyboard = types.InlineKeyboardMarkup()
    btn1_text = await TextButtonModel.get(id=1)
    btn2_text = await TextButtonModel.get(id=2)
    keyboard.add(types.InlineKeyboardButton(text=btn1_text.ru_text if language == 'ru' else btn1_text.eng_text, 
                                            callback_data="change_age:"))
    keyboard.add(types.InlineKeyboardButton(text=btn2_text.ru_text if language == 'ru' else btn2_text.eng_text, 
                                            callback_data="change_language:"))

    return keyboard



async def new_calculation_keyboard(language:str):
    keyboard = types.InlineKeyboardMarkup()

    btn_text = await TextButtonModel.get(id=11)
    btn_text = btn_text.ru_text if language == 'ru' else btn_text.eng_text
    keyboard.add(types.InlineKeyboardButton(btn_text,callback_data="back_general_location:"))
    return keyboard
# 