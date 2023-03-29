import asyncio
import secrets
from typing import List, Tuple
from aiogram import Router, F, Bot
# from aiogram.filters import or_f, in_
from aiogram.types import Message, CallbackQuery, BotCommand, LabeledPrice, SuccessfulPayment, PreCheckoutQuery, successful_payment, ContentType
from aiogram.filters import CommandStart, Command, Text, Filter, CommandObject
from aiogram.methods.send_message import SendMessage
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import decode_payload, create_deep_link, create_start_link, create_telegram_link

from const import PROMOCODE
from secret_data import TG_ADMIN_ID, TG_SUPPORT_ID
router = Router()  # [1]
from app.finite_state_machine import UserStates
from keyboards import BasicKeyboards as bkb
from keyboards import DynamicKeyboards as dkb


from processing.SQL_processingg.SQL_high_level_processing import get_lang, get_info_by_nickname, get_user_info_quickly
# from processing.casinoBackEnd import get_slot_machine_resul
from text_data.message_answers import answers_texts as ma_texts
from text_data import callback_answers
from aiogram.utils.deep_linking import create_start_link, encode_payload
from aiogram.types.labeled_price import LabeledPrice

from aiogram.types import Message

# from payments.config import YOOKASSA_TOKEN, GOODS
from payments.config import PRICE_LIST
import payments.pay_text_data as ptexts
import payments.config as payment_config

async def make_labels(goods: List[Tuple[str, int]]):
    """ Create a product catalog"""
    prices = [
        LabeledPrice(label=n, amount=m) for (n, m) in goods
    ]
    return list(prices)

async def get_price(product, payment_method):
    return PRICE_LIST.loc[product][payment_method]


async def begin_payment(message: Message, item: str, method: str, lang='en'):

    # methods = set()
    category, subcategory = item.split('-')
    value = payment_config.ALL_GOODS[category][subcategory]['value']
    method_info = ptexts.PAYMENT_METHODS_DESCRIPTION[method]
    if method_info['through_provider']:
        provider = method_info['provider_token']
        label = ptexts.PURCHASE_STEPS['description'][category][lang].format(value)
        price = payment_config.PRICE_LIST.loc[item][method] * 100
        # Transform int to LabelPrice
        payment_data = dict(
            title='титл',
            description='purchasing of {}'.format(category),
            payload=f"{category}-{value}-{secrets.token_hex(4)}",
            prices=await make_labels(goods=[(label, price), ]),
            currency=method.split('_')[0],
            provider_token=provider)

        # payment_data['prices'] = await make_labels(goods=[(label, price), ])
        # payment_info['provider_token'] = PAYMENT_METHODS[currency][type]['provider_token']
        link = encode_payload(str(
            # ИСПРАВИТЬ (ТУТ АЙДИ БОТА)
            message.from_user.id
        ))
        await message.answer_invoice(
            # **PAY_DATA,
            **payment_data,

            # If payment message is followed to other, button becomes referral link
            start_parameter=link,

            allow_sending_without_reply = True
        )
    else:
        # Payments through smth else, e.x. crypto
        await message.reply("ПЛОТИ",
            allow_sending_without_reply=True
        )
    await message.edit_text(ma_texts['market'][lang]+ptexts.PURCHASE_STEPS['waiting_for_payment'][lang])