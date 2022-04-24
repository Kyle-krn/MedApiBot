from collections import defaultdict
from multiprocessing import parent_process
from loader import dp
from aiogram import types
from models.models import BodyLocations, TextModel, UserModel, Symptoms, UserSymptoms
from keyboards.inline.med_keyboards import choice_body_sublocation, choice_body_location, choice_symptoms_keyboard, symptoms_control_keyboard, change_settings_keyboards
from tortoise.queryset import Q
from utils.medapi import api
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'back_general_location')
@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'clear')
async def back_general_location_handler(call: types.CallbackQuery):
    user = await UserModel.get(tg_id=call.message.chat.id)
    text = ''
    if call.data.split(':')[0] == 'clear':
        clear_text = await TextModel.get(id=12)
        clear_text = clear_text.ru_text if user.language == 'ru' else clear_text.eng_text
        text += f"{clear_text}\n\n"
    area_body_text = await TextModel.get(id=7)
    text += area_body_text.ru_text if user.language == 'ru' else area_body_text.eng_text
    return await call.message.edit_text(text, reply_markup=await choice_body_location(user.language))


@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'general_location')
async def general_location_handler(call: types.CallbackQuery):
    user = await UserModel.get(tg_id=call.message.chat.id)
    general_location_id = call.data.split(":")[1]
    location = await BodyLocations.get(id=general_location_id)
    sublocation = await location.location.all()
    location_name = location.ru_name if user.language == 'ru' else location.eng_name
    area_body_text = await TextModel.get(id=8)
    area_body_text = area_body_text.ru_text if user.language == 'ru' else  area_body_text.eng_text
    specify_area_text = await TextModel.get(id=9)
    specify_area_text = specify_area_text.ru_text if user.language == 'ru' else  specify_area_text.eng_text
    text = f"{area_body_text} <b>{location_name}</b>\n\n{specify_area_text}"
    return await call.message.edit_text(text=text, reply_markup=await choice_body_sublocation(language=user.language, sublocations=sublocation)) 



@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'sublocation')
async def symptoms_handler(call: types.CallbackQuery):
    user = await UserModel.get(tg_id=call.message.chat.id)
    sublocation_id = call.data.split(":")[2]
    sublocation = await BodyLocations.get(id=sublocation_id)
    sublocation_text = sublocation.ru_name if user.language == 'ru' else sublocation.eng_name
    parent_location = await sublocation.parent
    parent_location_text = parent_location.ru_name if user.language == 'ru' else parent_location.eng_name
    area_body_text = await TextModel.get(id=8)
    area_body_text = area_body_text.ru_text if user.language == 'ru' else area_body_text.eng_text
    specify_area_text = await TextModel.get(id=9)
    specify_area_text = specify_area_text.ru_text if user.language == 'ru' else  specify_area_text.eng_text
    text = f"{area_body_text} <b>{sublocation_text} -> {parent_location_text}</b>\n\n{specify_area_text}"
    
    page = int(call.data.split(":")[1])
    limit = 10
    offset = (page - 1) * limit
    symptoms_count = await sublocation.symptoms.all().count()
    max_page = (symptoms_count // limit) + 1 if symptoms_count % limit else  symptoms_count // limit
    
    symptoms = await sublocation.symptoms.all().offset(offset).limit(limit)
    return await call.message.edit_text(text=text, reply_markup=await choice_symptoms_keyboard(user=user, 
                                                                                               symptoms=symptoms, 
                                                                                               page=page, 
                                                                                               max_page=max_page,
                                                                                               sublocation_id=sublocation_id,
                                                                                               parent_location_id=parent_location.id))
# @dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'general_location')


@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'add_symptom')
async def add_symptom_handler(call: types.CallbackQuery):
    page = int(call.data.split(':')[1])
    sublocation_id = int(call.data.split(':')[2])
    sublocation = await BodyLocations.get(id=sublocation_id)
    symptom_id = int(call.data.split(':')[3])
    user = await UserModel.get(tg_id=call.message.chat.id)
    symptom = await Symptoms.get(id=symptom_id)
    user_symptoms = await user.symptoms.all()
    if symptom not in user_symptoms:
        await UserSymptoms.create(user=user, symptom=symptom, sublocation=sublocation)
        # await user.symptoms.add(symptom)
    else:
        await UserSymptoms.get(Q(user=user) & Q(symptom=symptom) & Q(sublocation=sublocation)).delete()
        # await user.symptoms.remove(symptom)
    call.data = f"sublocation:{page}:{sublocation_id}"
    return await symptoms_handler(call)


@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'apply_symptom')
@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'back_payments')
async def apply_symptom_handler(call: types.CallbackQuery):
    # print('here')
    user = await UserModel.get(tg_id=call.message.chat.id)
    symptoms_user = await UserSymptoms.filter(user=user)
    if len(symptoms_user) == 0:
        text = await TextModel.get(id=17)
        text = text.ru_text if user.language == 'ru' else text.eng_text
        return await call.answer(text)
        
    symptoms_text = await TextModel.get(id=11)
    symptoms_text = symptoms_text.ru_text if  user.language == 'ru' else symptoms_text.eng_text
    text = f"{symptoms_text}\n"
    defaultdict_sublocation = defaultdict(list)
    for symptom_user in symptoms_user:
        symptom = await symptom_user.symptom
        symptom_text = symptom.ru_name if user.language == 'ru' else symptom.eng_name
        sublocation = await symptom_user.sublocation
        sublocation_text = sublocation.ru_name if user.language == 'ru' else sublocation.eng_name
        parent_location = await sublocation.parent
        parent_location_text = parent_location.ru_name if user.language == 'ru' else parent_location.eng_name
        defaultdict_sublocation[f"{parent_location_text}:{sublocation_text}"].append(symptom_text)
        # text += f'{symptom_text} -> {sublocation_text} -> {parent_location_text}\n'
    for k,v  in defaultdict_sublocation.items():
        parent_location_text = k.split(':')[0]
        sublocation_text = k.split(':')[1]
        text += f"{parent_location_text} -> {sublocation_text}:\n"
        text += ", ".join(v)
        text += "\n\n"
    
    if call.data.split(':')[0] == 'back_payments':
        await call.message.delete()
        return await call.message.answer(text=text, reply_markup=await symptoms_control_keyboard(user.language))
    
    await call.message.edit_text(text=text, reply_markup=await symptoms_control_keyboard(user.language))
    

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'clear_symptoms')
async def clear_symptoms_handler(call: types.CallbackQuery):
    user = await UserModel.get(tg_id=call.message.chat.id)
    await UserSymptoms.filter(user=user).delete()
    call.data = 'clear:'
    return await back_general_location_handler(call)

    # find_diagnosis

# @dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'find_diagnosis')
@dp.message_handler(commands=['tests'])
async def find_diagnosis_handler(message: types.Message):
    user = await UserModel.get(tg_id=message.chat.id)
    text_message = await TextModel.get(id=14)
    text = text_message.ru_text if user.language == 'ru' else text_message.eng_text
    # print(text.format('a', 'b', 'c'))
    
    symptoms_list = str([17, 31])

    resp = await api.get_diagnosis(language='ru-ru' if user.language == 'ru' else 'en-gb', male=user.male, symptoms=symptoms_list, year_of_birth=user.year_of_birth)
    text = text.format(resp[0]['Issue']['Accuracy'], resp[0]['Issue']['Name'], ", ".join([i['Name'] for i in resp[0]['Specialisation']]))

    # spec = [i['Name'] for i in resp[0]['Specialisation']]
    print(text)
    # if resp == []:
    #     pass



@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'new_calculation')
# @dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'clear')
async def new_calculation_handler(call: types.CallbackQuery):
    user = await UserModel.get(tg_id=call.message.chat.id)
    text = ''
    area_body_text = await TextModel.get(id=7)
    text += area_body_text.ru_text if user.language == 'ru' else area_body_text.eng_text
    await call.message.edit_reply_markup(reply_markup=None)
    return await call.message.answer(text, reply_markup=await choice_body_location(user.language))
