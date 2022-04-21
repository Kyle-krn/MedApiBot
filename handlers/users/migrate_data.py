from aiogram import types
from utils.medapi import api
from loader import dp
from models.models import BodyLocations, Symptoms


@dp.message_handler(commands=['get_loc'])
async def get_locations(message: types.Message):
    if message.chat.id != 390442593:
        return
    ru_location = await api.get_body_locations(language="ru-ru")
    eng_location = await api.get_body_locations(language="en-gb")
    for ru_i in ru_location:
        eng_loc = [eng_i for eng_i in eng_location if eng_i['ID'] == ru_i["ID"]]
        await BodyLocations.create(id=ru_i['ID'], ru_name=ru_i["Name"], eng_name=eng_loc[0]['Name'])
    await message.answer("Успешно")


@dp.message_handler(commands=['get_subloc'])
async def get_sublocations(message: types.Message):
    if message.chat.id != 390442593:
        return
    # ru_sublocation = await api.get_body_sublocations(language="ru-ru", location_id=6)
    general_location = await BodyLocations.filter(parent_id__isnull=True)
    for location in general_location:
        ru_sublocations = await api.get_body_sublocations(language="ru-ru", location_id=location.id)
        eng_sublocations = await api.get_body_sublocations(language="en-gb", location_id=location.id)
        for ru_i in ru_sublocations:
            eng_subloc = [eng_i for eng_i in eng_sublocations if eng_i['ID'] == ru_i["ID"]]
            await BodyLocations.create(id=ru_i['ID'], ru_name=ru_i["Name"], eng_name=eng_subloc[0]['Name'], parent=location)
    await message.answer("Успешно")


@dp.message_handler(commands=['get_symptoms'])
async def get_symptoms(message: types.Message):
    if message.chat.id != 390442593:
        return
    locations = await BodyLocations.all()
    for location in locations:
        ru_symptoms = await api.get_symptoms(language='ru-ru', location_id=location.id, gender="girl")
        eng_symptoms = await api.get_symptoms(language='en-gb', location_id=location.id, gender="girl")
        for ru_symptom in ru_symptoms:
            sym_db = await Symptoms.filter(id=ru_symptom['ID'])
            if not sym_db:
                print(ru_symptoms)
                eng_symptom = [i for i in eng_symptoms if i['ID'] == ru_symptom['ID']]
                # print(eng_symptom)
                sym_db = await Symptoms.create(id=ru_symptom['ID'], 
                                            ru_name=ru_symptom['Name'], 
                                            eng_name=eng_symptom[0]['Name'], 
                                            has_red_flag=ru_symptom['HasRedFlag'],
                                            ru_synonyms=ru_symptom['Synonyms'],
                                            eng_synonyms=eng_symptom[0]['Synonyms'],)
                for i in ru_symptom['HealthSymptomLocationIDs']:
                    # try:
                    location = await BodyLocations.get(id=i)
                    # except:
                    await sym_db.locations.add(location)
    await message.answer("Успешно")


@dp.message_handler(commands=['symptoms'])
async def test(message: types.Message):
    x = await Symptoms.get(id=9)
    print(x)
    print(await x.locations.all())