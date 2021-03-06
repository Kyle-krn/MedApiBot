from datetime import datetime
from handlers.users.med_handlers import apply_symptom_handler
from loader import dp
from aiogram import types
from models.models import UserModel, TextModel
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyboards import change_gender_keyboard, language_keyboard
from keyboards.inline.med_keyboards import choice_body_location, change_settings_keyboards
from aiogram.dispatcher.filters import Text

class UserSettingsState(StatesGroup):
    age = State()
    
    location_country = State()
    location_city = State()


# @dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'change_language')
# @dp.message_handler(lambda message: message.text == '')
@dp.message_handler(Text(equals=["Изменить язык"]))
@dp.message_handler(Text(equals=["Change language"]))
async def change_language(message: types.Message):
    user = await UserModel.get(tg_id=message.chat.id)
    language_text = await TextModel.get(id=2)
    language_text = language_text.ru_text if user.language else language_text.eng_text
    await message.answer(language_text, reply_markup=await language_keyboard(first=False))




@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'language')
@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'set_language')
async def choice_language(call: types.CallbackQuery):
    language = call.data.split(':')[1]
    user = await UserModel.get(tg_id=call.message.chat.id)
    user.language = language
    await user.save()
    
    if call.data.split(':')[0] == 'set_language':
        text = await TextModel.get(id=22)
        text = text.ru_text if user.language == 'ru' else text.eng_text
        await call.message.delete()
        return await call.message.answer(text, reply_markup=await change_settings_keyboards(user.language))
        # call.data = "apply_symptom:"
        # return await apply_symptom_handler(call)

    birth_text = await TextModel.get(id=3)
    text = birth_text.ru_text if user.language == 'ru' else birth_text.eng_text
    await UserSettingsState.age.set()
    state = dp.get_current().current_state()
    await state.update_data(first=True)
    await call.message.edit_text(text)


@dp.message_handler(Text(equals=["Изменить пол и возраст"]))
@dp.message_handler(Text(equals=["Change gender and age"]))
async def change_age_handler(message: types.Message):
    user = await UserModel.get(tg_id=message.chat.id)
    birth_text = await TextModel.get(id=3)
    text = birth_text.ru_text if user.language == 'ru' else birth_text.eng_text
    await UserSettingsState.age.set()
    state = dp.get_current().current_state()
    await state.update_data(first=False)
    await message.answer(text)

# @dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'change_age')
# async def change_age_handler(call: types.CallbackQuery):
#     user = await UserModel.get(tg_id=call.message.chat.id)
#     birth_text = await TextModel.get(id=3)
#     text = birth_text.ru_text if user.language == 'ru' else birth_text.eng_text
#     await UserSettingsState.age.set()
#     state = dp.get_current().current_state()
#     await state.update_data(first=False)
#     await call.message.edit_text(text)

@dp.message_handler(state=UserSettingsState.age)
async def input_age(message: types.Message, state: FSMContext):
    user = await UserModel.get(tg_id=message.chat.id)
    user_data = await state.get_data()
    invalid_age_text = await TextModel.get(id=4)
    invalid_age_text = invalid_age_text.ru_text if user.language == 'ru' else invalid_age_text.eng_text
    if message.text.isdigit():
        age = int(message.text)
        age = datetime.now().year - age
        if (1900 < age < 2022) is False:
            return await message.answer(invalid_age_text)
        user.year_of_birth = age
        await user.save()
        await state.finish()
        gender_text = await TextModel.get(id=5)
        gender_text = gender_text.ru_text if user.language == 'ru' else gender_text.eng_text
        
        return await message.answer(gender_text, reply_markup=await change_gender_keyboard(user.language, first=user_data['first']))
    else:
        return await message.answer(invalid_age_text)


@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'gender')
@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'set_gender')
async def change_gender(call: types.CallbackQuery):
    user = await UserModel.get(tg_id=call.message.chat.id)
    gender = call.data.split(':')[1]
    if gender == 'male':
        user.male = True
        gender_text = await TextModel.get(id=19)
    if gender == 'female':
        user.male = False
        gender_text = await TextModel.get(id=18)
    await user.save()
    gender_text = gender_text.ru_text if user.language == 'ru' else gender_text.eng_text
    await call.answer(gender_text)
    if not user.location_country:
        await UserSettingsState.location_country.set()
        location_text = await TextModel.get(id=6)
        location_text = location_text.ru_text if user.language == 'ru' else location_text.eng_text
        return await call.message.edit_text(location_text)
    else:
        if call.data.split(':')[0] == 'set_gender':
            return await call.message.delete()
            # call.data = "apply_symptom:"
            # return await apply_symptom_handler(call)

        area_body_text = await TextModel.get(id=7)
        area_body_text = area_body_text.ru_text if user.language == 'ru' else area_body_text.eng_text
        return await call.message.edit_text(area_body_text, reply_markup=await choice_body_location(user.language))





@dp.message_handler(state=UserSettingsState.location_country)
async def set_location(message: types.Message, state: FSMContext):
    user = await UserModel.get(tg_id=message.chat.id)
    user.location_country = message.text
    await user.save()
    await UserSettingsState.location_city.set()
    city_text = await TextModel.get(id=23)
    city_text = city_text.ru_text if user.language == 'ru' else city_text.eng_text
    return await message.answer(city_text)
    # await state.finish()
    area_body_text = await TextModel.get(id=7)
    area_body_text = area_body_text.ru_text if user.language == 'ru' else area_body_text.eng_text
    return await message.answer(area_body_text, reply_markup=await choice_body_location(user.language))

@dp.message_handler(state=UserSettingsState.location_city)
async def set_location(message: types.Message, state: FSMContext):
    user = await UserModel.get(tg_id=message.chat.id)
    user.location_city = message.text
    await user.save()
    # await UserSettingsState.location_city.set()
    # city_text = await TextModel.get(id=23)
    # city_text = city_text.ru_text if user.language == 'ru' else city_text.eng_text
    await state.finish()
    area_body_text = await TextModel.get(id=7)
    area_body_text = area_body_text.ru_text if user.language == 'ru' else area_body_text.eng_text
    return await message.answer(area_body_text, reply_markup=await choice_body_location(user.language))