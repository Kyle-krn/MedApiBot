from keyboards.inline.med_keyboards import new_calculation_keyboard
from loader import dp, bot
from data.config import PAYMENTS_TOKEN
from aiogram import types
from models.models import TextModel, UserModel, SuccessPayments, UserSymptoms, SettingsPayments
from keyboards.inline.keyboards import payments_keyboard
from utils.medapi import api

@dp.callback_query_handler(lambda call: call.data.split(':')[0] == 'find_diagnosis')
async def payments_order(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    pay_settings = await SettingsPayments.get(id=1)
    user = await UserModel.get(tg_id=call.message.chat.id)
    label = pay_settings.ru_label if user.language == 'ru' else pay_settings.eng_label
    # amount = pay_settings.amount
    prices = [types.LabeledPrice(label=label, amount=pay_settings.amount)]
    
    text_message = await TextModel.get(id=13)
    text = text_message.ru_text if user.language == 'ru' else text_message.eng_text
    text = text.format(int(pay_settings.amount / 100))
    title_text = await TextModel.get(id=16)
    title_text = text_message.ru_text if user.language == 'ru' else text_message.eng_text
    msg = await bot.send_invoice(call.message.chat.id,
                           title=title_text,
                           description=text,
                           provider_token=PAYMENTS_TOKEN,
                           currency='rub',
                           photo_url=pay_settings.url_photo,
                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           photo_size=512, 
                           is_flexible=False,  # True If you need to set up Shipping Fee
                           prices=prices,
                           start_parameter='example',
                           need_name=False,
                           need_shipping_address=False,
                           need_phone_number=False,
                           payload=f"pp",
                           reply_markup=await payments_keyboard(user.language))
    print(msg.message_id)


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")



@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    user = await UserModel.get(tg_id=message.chat.id)
    symptoms_list = list(set([i.id for i in await user.symptoms.all()]))
    resp = await api.get_diagnosis(language='ru-ru' if user.language == 'ru' else 'en-gb', 
                                male=user.male, 
                                symptoms=symptoms_list, 
                                year_of_birth=user.year_of_birth)
    await bot.delete_message(message.chat.id, message.message_id-1)
    print(resp)
    if resp == []:
        text = await TextModel.get(id=15)
        text = text.ru_text if user.language == 'ru' else text.eng_text
    else:
        text = await TextModel.get(id=14)
        text = text.ru_text if user.language == 'ru' else text.eng_text
        text = text.format(resp[0]['Issue']['Accuracy'], resp[0]['Issue']['Name'], ", ".join([i['Name'] for i in resp[0]['Specialisation']]))
    pmnt = message.successful_payment
    amount = pmnt.total_amount / 100

    await SuccessPayments.create(user=user, symptom_array=symptoms_list, diagnosis=text, amount=amount)
    await UserSymptoms.filter(user=user).delete()
    
    await bot.send_message(
        message.chat.id,
        text,
        reply_markup=await new_calculation_keyboard(user.language, "new_calculation:")
        )
    