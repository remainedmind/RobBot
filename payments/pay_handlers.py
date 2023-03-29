
import secrets

from aiogram import Router, F, Bot, md

from aiogram.types import Message, CallbackQuery, BotCommand, LabeledPrice, SuccessfulPayment, PreCheckoutQuery, successful_payment, ContentType, TelegramObject
from aiogram.filters import CommandStart, Command, Text, Filter, CommandObject
from aiogram.methods.send_message import SendMessage
from aiogram.methods.send_photo import SendPhoto
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import decode_payload, create_deep_link, create_start_link, create_telegram_link

from const import PROMOCODE
from secret_data import TG_ADMIN_ID, TG_SUPPORT_ID, PAYMENTS_REQUISITIES_DATA
router = Router()  # [1]
from app.finite_state_machine import UserStates
from keyboards import BasicKeyboards as bkb
from keyboards import DynamicKeyboards as dkb
from aiogram.utils.deep_linking import create_start_link, encode_payload

from processing.SQL_processingg.SQL_high_level_processing import get_lang, get_info_by_nickname, get_user_info_quickly
# from processing.casinoBackEnd import get_slot_machine_resul
from text_data.message_answers import answers_texts as ma_texts, admin_command_answers
from processing.SQL_processingg import SQL_high_level_processing as sql_high_p
from text_data import callback_answers
from text_data.various import expiry_format


# from payments.pay_keyboards import get_invoice, get_invoice_button
import payments.pay_keyboards as pkb
from payments.pay_text_data import PAYMENT_CURRENCIES_DESCRIPTION, PAYMENT_METHODS_DESCRIPTION, PURCHASE_STEPS
import payments.pay_text_data as ptexts
# from payments.config import ALL_GOODS
import payments.config as payment_config
from payments.pay_processing import get_price, make_labels
# from payments.pay_keyboards import market_kb, options_kb
# from payments.pay_keyboards import PaymentsCallback, get_buy_keyboard
# @router.message(F.content_type.in_({ContentType.SUCCESSFUL_PAYMENT, }))
from processing.timeProcessing import get_expiry_date


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def handle_successfull_payment(
        # payment: SuccessfulPayment,
        message: Message,
        state: FSMContext,

):
    lang = (await state.get_data())['language']
    user_id = message.from_user.id
    # print(SuccessfulPayment)
    # print(message.date.utcnow(), message.successful_payment, sep='\n\n')
    payment = message.successful_payment
    payload = payment.invoice_payload
    now = message.date.utcnow()
    confirm = await sql_high_p.confirm_payment(
        user_id=user_id,
        payload = payload,
        now =now
    )
    if confirm:
        # last from right piece of payload is unique payment value. We don't need it
        item, value, _ = payload.split(sep='-')
        if item == 'coins':
            put = await sql_high_p.change_coins_balance(user_id, charge=int(value), method='put')
            if put:
                await message.answer(ma_texts['got_coins'][lang].format(value))
        elif item == 'sub':
            success = await sql_high_p.set_new_status(user_id, 'premium', now)
            if success:
                await message.reply(ma_texts['new_status']['premium'][lang])
    else:
        await message.reply(ma_texts['payment_failed'][lang])


@router.pre_checkout_query()
async def handle_precheckout(
        query: PreCheckoutQuery,

):
    user = query.from_user
    new_payment = await sql_high_p.add_new_payment(
        query_id=query.id,
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        second_name=user.last_name,
        currency=query.currency,
        price=query.total_amount,
        payload=query.invoice_payload
    )
    if new_payment:
        await query.answer(ok=True)


@router.callback_query(F.data == 'cancel')
async def callbacks_num_change_fab(
        callback: CallbackQuery,
        state: FSMContext
):
    lang = (await state.get_data())['language']
    await state.set_state(UserStates.main)
    await callback.answer(callback_answers.forget_action[lang])
    await callback.message.delete_reply_markup()
# await callback.message.edit_reply_markup(reply_markup=bkb.setting_kb[lang])



@router.callback_query(pkb.PaymentsCallback.filter())
async def callbacks_num_change_fab(
        callback: CallbackQuery,
        callback_data: pkb.PaymentsCallback,
        state: FSMContext,
        bot: Bot
):
    await state.set_state(UserStates.main)
    lang = (await state.get_data())['language']
    text = ma_texts['market'][lang]
    user_id = callback.from_user.id
    markup = None
    subject, value, action, item, data, price, currency = callback_data.subject, callback_data.value, callback_data.action, callback_data.item, callback_data.data, callback_data.price, callback_data.currency
    print(subject, value, action, item, data, price, currency)
    if item:
        category, subcategory = item.split('-')
    if action == 'show':  # Показать текущее значение или доступные варианты
        if subject == 'all_goods':
            text += PURCHASE_STEPS['description_of_product'][data][lang]
            markup = pkb.options_kb[data][lang]
        elif subject == 'specific_product':
            # print(ptexts.description_of_product, category)
            text += ptexts.product_synonym[lang].format(
                ptexts.product_description[category][lang].format(
                payment_config.ALL_GOODS[category][subcategory]['value'])
            )
                                                               # payment_config.ALL_GOODS[category][subcategory]['value'
            text += ptexts.go_next[lang]

            # markup = await pkb.get_buy_keyboard(data=data, value=value, currency=currency, price=price, lang=lang)
            markup = await pkb.get_buy_button(item=item, lang=lang)
        elif subject == 'payment_ways':

            # markup = await pkb.get_buy_keyboard(data=data, value=value, currency=currency, price=price, lang=lang)
            text += PURCHASE_STEPS['choose_payment_method'][lang]
            # text += ptexts.description_of_product

            markup = await pkb.get_available_payment_ways(item=item, lang=lang)
        elif subject == 'payment_methods':
            text += PURCHASE_STEPS['choose_payment_method'][lang]
            markup = await pkb.get_specific_payment_methods(item=item, currency=currency, lang=lang)
        elif subject == 'info':
            if data == 'restriction_reason':
                markup = pkb.market_kb[lang]
                # await callback.message.edit_reply_markup(reply_markup=market_kb[lang])
                await callback.answer(callback_answers.restriction_reason_in_market[lang], show_alert=True)

    elif action == 'back_to':
        if subject == 'market':
            markup = pkb.market_kb[lang]
        # elif subject == 'all_goods':
        #     markup = pkb.options_kb[data][lang]

    elif action == 'buy':

        reject = None
        if category == 'sub':
            # We check is user already has Premium
            if await sql_high_p.check_for_premium(user_id) == 'premium':
                reject = True


        if not reject:
            text += ptexts.product_synonym[lang].format(
                ptexts.product_description[category][lang].format(
                    payment_config.ALL_GOODS[category][subcategory]['value'])
            )
            text += ptexts.payment_method[lang].format(
                PAYMENT_METHODS_DESCRIPTION[subject]['description'][lang]
            )

            price = await get_price(item, payment_method=subject)
            price_and_currency = ptexts.currency[currency].format(price)

            text += ptexts.price[lang].format(price_and_currency)
            # text += payment_config.ALL_GOODS[category][subcategory]['price'].format(
            #     payment_config.price_format_for_each_currency[currency][lang].format(price)
            # )

            markup = await pkb.get_pay_button(item=item, currency=currency, method=subject, lang=lang)
        else:
            markup = pkb.market_kb[lang]
            text += PURCHASE_STEPS['already_has_sub'][lang]

    elif action == 'pay':
        method = subject

        # price = await get_price(item, payment_method=subject)
        # text += payment_config.ALL_GOODS[category][subcategory]['price'].format(
        #     payment_config.price_format_for_each_currency[currency][lang].format(price)
        # )
        #
        price = await get_price(item, payment_method=subject)
        price_and_currency = ptexts.currency[currency].format(price)


        value = payment_config.ALL_GOODS[category][subcategory]['value']
        method_info = ptexts.PAYMENT_METHODS_DESCRIPTION[method]
        currency = method.split('_')[0]
        payload = f"{category}-{value}-{secrets.token_hex(8)}"
        if method_info['through_provider']:
            provider = method_info['provider_token']
            label = ptexts.goods_description[category][lang].format(value)
            price = payment_config.PRICE_LIST.loc[item][method] * 100
            # Transform int to LabelPrice
            payment_data = dict(
                title=PURCHASE_STEPS['invoice_description']['title'][lang],
                description=PURCHASE_STEPS['invoice_description']['description'][category][lang].format(value),
                payload=payload,
                prices=await make_labels(goods=[(label, price), ]),
                currency=currency,
                provider_token=provider)

            # payment_data['prices'] = await make_labels(goods=[(label, price), ])
            # payment_info['provider_token'] = PAYMENT_METHODS[currency][type]['provider_token']

            # Referral link
            link = encode_payload(str(user_id))
            await callback.message.answer_invoice(
                # **PAY_DATA,
                **payment_data,

                # If payment message is followed to other, button becomes referral link
                start_parameter=link,

                allow_sending_without_reply=True
            )
        elif method == 'BOT_BALANCE':
            # price = await get_price(item, payment_method=subject)
            # price_and_currency = ptexts.currency[currency].format(price)
            # text += payment_config.ALL_GOODS[category][subcategory]['price'].format(
            #     payment_config.price_format_for_each_currency[currency][lang].format(price)
            # )
            # print(text)
            text += ptexts.product_synonym[lang].format(
                ptexts.product_description[category][lang].format(
                payment_config.ALL_GOODS[category][subcategory]['value'])
            )
            markup = await pkb.buy_with_balance(item, currency, method, lang)
            # text += payment_config.ALL_GOODS[category][subcategory]['price'].format(payment_config.price_format_for_each_currency[currency][lang].format(price))
            # markup = await pkb.get_pay_button(item=item, currency=currency, method=subject, lang=lang)
        else:

            new_payment = await sql_high_p.add_new_payment(
                query_id=callback.id,
                user_id=user_id,
                username=callback.from_user.username,
                first_name=callback.from_user.first_name,
                second_name=callback.from_user.last_name,
                currency=currency,
                price=price,
                payload=payload
            )
            if new_payment:
                await state.set_state(UserStates.sending_receipt)
                await state.update_data(payload=payload)
                # Payments through smth else, e.x. crypto

                # price_and_currency = ptexts.currency[currency].format(price)

                text += ptexts.PURCHASE_STEPS['waiting_for_payment'][lang]
                second_text = (
                                      ptexts.product_synonym[lang].format(
                    ptexts.product_description[category][lang].format(
                        payment_config.ALL_GOODS[category][subcategory]['value'])
                ) + ptexts.price[lang].format(
                    price_and_currency)
                    + ptexts.show_requisites[lang].format(
                    PAYMENT_METHODS_DESCRIPTION[subject]['requisite']
                ) + ptexts.PURCHASE_STEPS['waiting_for_receipt'][lang]
                )

                if method == 'RUB_BANK_TRANSFER':
                    markup = await pkb.get_tinkoff_buy_button(item, currency, lang)
                else:
                    markup = await pkb.get_cancel_payment_button(item, currency, lang)

                await callback.message.reply(second_text,
                    reply_markup=markup,
                    allow_sending_without_reply=True
                )
                markup = None


    elif action == 'approve':
        # This action is for ADMIN
        user_id = subject
        payload = data

        item, value, _ = payload.split(sep='-')
        if item == 'coins':
            success = await sql_high_p.change_coins_balance(user_id, charge=int(value), method='put')
            if success:
                send_result = SendMessage(chat_id=user_id, text=ma_texts['got_coins'][lang].format(value))
                await callback.message.reply(admin_command_answers['new_balance'].format(value))
        elif item == 'sub':
            status = 'premium'
            now = callback.message.date.utcnow()  # UTC TIME

            success = await sql_high_p.set_new_status(user_id, status, now, period = {'days': int(value)})
            if success:
                send_result = SendMessage(chat_id=user_id, text=ma_texts['new_status'][status]['en'])
                await callback.message.reply(admin_command_answers['new_status'].format(status))
        if success:
            confirm = await sql_high_p.confirm_payment(
                user_id=user_id,
                payload=payload,
                now=callback.message.date.utcnow()
            )
            if confirm:
                await send_result
                text = None
                markup = None
        else:
            await callback.message.reply("AN ERROR OCCURED")

    elif action == 'confirm':
        # This action is for buying with BOTcoins
        value = payment_config.ALL_GOODS[category][subcategory]['value']
        price = await get_price(item, payment_method=subject)
        print(value, type(value), type(price), subject)

        if category == 'sub':
            status = 'premium'
            now = callback.message.date.utcnow()  # UTC TIME
            success = await sql_high_p.change_coins_balance(
                id=user_id, charge=price, method='buy'
            )
            if success:
                success = await sql_high_p.set_new_status(user_id, status, now, period = {'days': int(value)})
            else:
                text += ptexts.PURCHASE_STEPS['insufficient_balance'][lang]
                markup = pkb.sub_buying_failed_kb[lang]

            if success:
                # message about status is changed
                text += ma_texts['new_status'][status][lang]


    if text:
        await callback.message.edit_text(text=text, reply_markup=markup)
    else:
        await callback.message.edit_reply_markup(reply_markup=markup)


@router.message(UserStates.sending_receipt, F.photo)
async def photo_msg(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_info = await state.get_data()
    lang = user_info['language']
    payload = user_info['payload']

    item, value, _ = payload.split(sep='-')
    keyboard = await pkb.button_for_admin(
        payload=payload, user_id=user_id
    )
    db_info = await sql_high_p.get_user_info_quickly(user_id)

    db_info['balance'] = md.quote(str(db_info['balance']))  # in case it's negative
    if db_info['prem_expires']:
        expiry = await get_expiry_date(db_info['prem_expires'])
        db_info['prem_expires'] = md.quote(expiry.strftime(expiry_format['status_until']['en']))
    db_info['payment'] = f"{item}, {value}"
    payment_message = admin_command_answers[
        'payment_from'
    ].format(**db_info)

    await SendPhoto(chat_id=TG_SUPPORT_ID, photo=message.photo[0].file_id, caption=payment_message, parse_mode='MarkdownV2', reply_markup=keyboard)

    # await SendMessage(chat_id=TG_SUPPORT_ID, text=payment_message, parse_mode='MarkdownV2', reply_markup=keyboard)
    await state.set_state(UserStates.main)
    await message.answer(PURCHASE_STEPS['catch_screenshot'][lang])

@router.message(UserStates.sending_receipt)
async def photo_msg(message: Message, state: FSMContext):
    user_info = await state.get_data()
    lang = user_info['language']

    await message.answer(PURCHASE_STEPS['complete_the_payment'][lang])



