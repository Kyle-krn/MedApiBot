from loader import dp
from aiogram import types
from models.models import UserModel, TextModel
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyboards import change_gender_keyboard
from keyboards.inline.med_keyboards import choice_body_location

class UserSettingsState(StatesGroup):
    age = State()
    location = State()


@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'language')
async def choice_language(call: types.CallbackQuery):
    language = call.data.split(':')[1]
    user = await UserModel.get(tg_id=call.message.chat.id)
    user.language = language
    await user.save()
    birth_text = await TextModel.get(id=3)
    text = birth_text.ru_text if user.language == 'ru' else birth_text.eng_text
    await UserSettingsState.age.set()
    await call.message.edit_text(text)
    

@dp.message_handler(state=UserSettingsState.age)
async def input_age(message: types.Message, state: FSMContext):
    user = await UserModel.get(tg_id=message.chat.id)
    invalid_age_text = await TextModel.get(id=4)
    invalid_age_text = invalid_age_text.ru_text if user.language == 'ru' else invalid_age_text.eng_text
    if message.text.isdigit():
        age = int(message.text)
        if (1900 < age < 2022) is False:
            return await message.answer(invalid_age_text)
        user.year_of_birth = age
        await user.save()
        await state.finish()
        gender_text = await TextModel.get(id=5)
        gender_text = gender_text.ru_text if user.language == 'ru' else gender_text.eng_text
        return await message.answer(gender_text, reply_markup=await change_gender_keyboard(user.language))
    else:
        return await message.answer(invalid_age_text)


@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'gender')
async def change_gender(call: types.CallbackQuery):
    user = await UserModel.get(tg_id=call.message.chat.id)
    gender = call.data.split(':')[1]
    if gender == 'male':
        user.male = True
    if gender == 'female':
        user.male = False
    await user.save()
    if not user.location:
        await UserSettingsState.location.set()
        location_text = await TextModel.get(id=6)
        location_text = location_text.ru_text if user.language == 'ru' else location_text.eng_text
        return await call.message.edit_text(location_text)
    else:
        area_body_text = await TextModel.get(id=7)
        area_body_text = area_body_text.ru_text if user.language == 'ru' else area_body_text.eng_text
        return await call.message.edit_text(area_body_text, reply_markup=await choice_body_location(user.language))





@dp.message_handler(state=UserSettingsState.location)
async def set_location(message: types.Message, state: FSMContext):
    user = await UserModel.get(tg_id=message.chat.id)
    user.location = message.text
    await user.save()
    await state.finish()
    area_body_text = await TextModel.get(id=7)
    area_body_text = area_body_text.ru_text if user.language == 'ru' else area_body_text.eng_text
    return await message.answer(area_body_text, reply_markup=await choice_body_location(user.language))
