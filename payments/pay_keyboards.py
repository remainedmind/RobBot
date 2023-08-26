from typing import Union, Tuple, List, Optional
from aiogram.filters.callback_data import CallbackData

from aiogram.types import Message
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.create_invoice_link import CreateInvoiceLink
from text_data.message_answers import answers_texts as ma_texts


from payments.pay_processing import make_labels
# from payments.pay_text_data import goods_description, waiting_for_payment

from aiogram.utils.deep_linking import create_start_link, encode_payload
import payments.config as shop_config
import payments.pay_text_data as ptexts



class PaymentsCallback(CallbackData, prefix="payments"):
    """
    """
    action: Optional[str]  = None # Show | Pay | Back
    type: Optional[str]  = None # type of goods | type of action
    data: Optional[str]  = None # info
    subject: Optional[str]  = None # Out target to show, buy, e.t.c
    payment_method: Optional[str] = None
    currency: Optional[str] = None
    price: Optional[int] = None
    value: Optional[int] = None
    item: Optional[str]  = None  # Type of product


options_kb = {
    'coins': {
        'en':  InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="\U0001F4B5 100000 coins", callback_data=PaymentsCallback(
                    action='show',
                    subject='specific_product',
                    item='coins-1'

                ).pack())],
                [InlineKeyboardButton(text="\U0001F4B5 200000 coins", callback_data=PaymentsCallback(
                    action='show',
                    subject='specific_product',
                    item='coins-2'
                ).pack())],
                [InlineKeyboardButton(text="⬅ Back",
                                      callback_data=PaymentsCallback(
                                          action='back_to', subject='market', item=None
              ).pack())],
            ]
    ),
        'ru':  InlineKeyboardMarkup(inline_keyboard =[
            [InlineKeyboardButton(text="\U0001F4B5 50000 coins", callback_data=PaymentsCallback(
                action='show',
                subject='specific_product',
                item='coins-0').pack())],
                [InlineKeyboardButton(text="\U0001F4B5 100000 coins", callback_data=PaymentsCallback(
                    action='show',
                    subject='specific_product',
                    item='coins-1').pack())],
                [InlineKeyboardButton(text="\U0001F4B5 200000 coins", callback_data=PaymentsCallback(
                    action='show',
                    subject='specific_product',
                    item='coins-2').pack())],
                [InlineKeyboardButton(
                    text="⬅ Back",
                    callback_data=PaymentsCallback(
                        action='back_to', subject='market', item=None
                    ).pack())],
                # [InlineKeyboardButton(text="⬅ Back", callback_data="market")]
            ]
    ),
    },
    'sub': {
        'en': InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="💎 for 1 month", callback_data=PaymentsCallback(
                    action='show',
                    subject='specific_product',
                    item='sub-1'
                ).pack())],
                [InlineKeyboardButton(text="💎 for 2 month", callback_data=PaymentsCallback(
                    action='show',
                    subject='specific_product',
                    item='sub-2'
                ).pack())],
                [InlineKeyboardButton(text="⬅ Back", callback_data=PaymentsCallback(action='back_to', subject='market', item=None).pack())],
            ]
    ),
        'ru': InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="💎 1 месяц", callback_data=PaymentsCallback(
                    action='show',
                    subject='specific_product',
                    item='sub-1',
                   ).pack())],
                [InlineKeyboardButton(text="💎 2 месяца", callback_data=PaymentsCallback(
                    action='show',
                    subject='specific_product',
                    item='sub-2'
                ).pack())],
                [InlineKeyboardButton(text="⬅ Назад", callback_data=PaymentsCallback(action='back_to', subject='market', item=None).pack())],
            ]
    )
    }
}

buy_sub_kb = {
    'user':  {
        'en': InlineKeyboardMarkup(inline_keyboard =[
            [InlineKeyboardButton(text="Increase limit by 2 times", callback_data=PaymentsCallback(action='show', subject='all_goods', data='sub').pack())],

        ]
        ),
            'ru': InlineKeyboardMarkup(inline_keyboard =[
            [InlineKeyboardButton(text="Увеличить лимит в 2 раза", callback_data=PaymentsCallback(action='show', subject='all_goods', data='sub').pack())],
                ]
        ),
    },
    'premium': None
}


first_market_opening_kb = {
    'en': InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="\U0001F4B5	 More BOTcoins", callback_data=PaymentsCallback(action='show', subject='all_goods', data='coins').pack())],
                [InlineKeyboardButton(text="💎 Premium subcription", callback_data=PaymentsCallback(action='show', subject='all_goods', data='sub').pack())],
                [InlineKeyboardButton(text="⁉ Why do I have to pay?", callback_data=PaymentsCallback(action='show', subject='info', data='restriction_reason').pack())],
                [InlineKeyboardButton(text="⬅ Back", callback_data="main")]
        ]
    ),
    'ru': InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="\U0001FA99 Больше БОТкоинов", callback_data=PaymentsCallback(action='show', subject='all_goods', data='coins').pack())],
                [InlineKeyboardButton(text="💎 Премиум-подписка", callback_data=PaymentsCallback(action='show', subject='all_goods', data='sub').pack())],
                [InlineKeyboardButton(text="⁉ Платить? За что?", callback_data=PaymentsCallback(action='show', subject='info', data='restriction_reason').pack())],
                [InlineKeyboardButton(text="⬅ Назад", callback_data="main",)]
        ]
    )
}


market_kb = {
    'en': InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="\U0001FA99 More BOTcoins", callback_data=PaymentsCallback(action='show', subject='all_goods', data='coins').pack())],
                [InlineKeyboardButton(text="💎 Premium subcription", callback_data=PaymentsCallback(action='show', subject='all_goods', data='sub').pack())],
                [InlineKeyboardButton(text="⬅ Back", callback_data="main")]
        ]
    ),
    'ru': InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="\U0001FA99 Больше БОТкоинов", callback_data=PaymentsCallback(action='show', subject='all_goods', data='coins').pack())],
                [InlineKeyboardButton(text="💎 Премиум-подписка", callback_data=PaymentsCallback(action='show', subject='all_goods', data='sub').pack())],
                [InlineKeyboardButton(text="⬅ Назад", callback_data="main")]
        ]
    )
}

async def get_buy_button(item: str, lang='en'):

    builder = InlineKeyboardBuilder()
    buy_text = '➡ Купить' if lang == 'ru' else '➡ Buy'
    builder.button(text=buy_text, callback_data=PaymentsCallback(action='show', subject='payment_ways', item=item))
    cancel_text = '⬅ Назад' if lang =='ru' else '⬅ Back'
    builder.button(text=cancel_text, callback_data=PaymentsCallback(action='show', subject='all_goods', data=item.split('-')[0]))
    builder.adjust(1)
    return builder.as_markup()


async def get_available_payment_ways(item: str, lang='en'):
    """
    Fucntion to show all available ways to pay for certain good,
    e.x. USD, RUB, Crypto
    :param methods:
    :param lang:
    :return:
    """
    builder = InlineKeyboardBuilder()
    currencies = set()
    type, number = item.split('-')
    available_methods = shop_config.ALL_GOODS[type][number]['supported_payments']
    for method in available_methods:
        # We add first key of method - its currency
        currencies.add(method.split('_')[0])

    for cur in currencies:
        text = ptexts.SUPPORTED_WAYS_TO_PAY[cur][lang]
        builder.button(text=text, callback_data=PaymentsCallback(action='show', subject='payment_methods', item=item, currency=cur))
        # builder.button(text=texts[1], callback_data='main')

    cancel_text = '⬅ Назад' if lang =='ru' else '⬅ Back'

    # builder.button(text=cancel_text, callback_data='market')
    # builder.button(text=cancel_text, callback_data=PaymentsCallback(action='back_to', subject='all_goods'))
    builder.button(text=cancel_text, callback_data=PaymentsCallback(action='show', subject='specific_product', item=item))
    builder.adjust(1)
    return builder.as_markup()


async def get_specific_payment_methods(item: str, currency: str, lang='en'):
    """
    Fucntion to show all available ways to pay for certain good,
    e.x. USD, RUB, Crypto
    :param methods:
    :param lang:
    :return:
    """
    builder = InlineKeyboardBuilder()
    # methods = set()
    type, number = item.split('-')
    available_methods = shop_config.ALL_GOODS[type][number]['supported_payments']

    for method in available_methods:
        if method.split('_')[0] == currency:
            # We add only methods with currency matching
            text = ptexts.PAYMENT_METHODS_DESCRIPTION[method]['name'][lang]
            builder.button(text=text, callback_data=PaymentsCallback(action='buy', subject=method, item=item,
                                                                     currency=currency))


    cancel_text = '⬅ Назад' if lang == 'ru' else '⬅ Back'

    # builder.button(text=cancel_text, callback_data='market')
    # builder.button(text=cancel_text, callback_data=PaymentsCallback(action='back_to', subject='all_goods'))
    builder.button(text=cancel_text,
                   callback_data=PaymentsCallback(action='show', subject='payment_ways', item=item, currency=currency))
    builder.adjust(1)
    return builder.as_markup()


async def buy_with_balance(item: str, currency: str, method: str, lang='en'):
    """
    Fucntion to show all available ways to pay for certain good,
    e.x. USD, RUB, Crypto
    :param methods:
    :param lang:
    :return:
    """
    builder = InlineKeyboardBuilder()
    confirm_text = '✅ Подтвердить' if lang == 'ru' else '✅ Confirm'
    builder.button(text=confirm_text, callback_data=PaymentsCallback(action='confirm', item=item, subject=method))

    cancel_text = '❌ Отменить' if lang == 'ru' else '❌ Cancel'

    # builder.button(text=cancel_text, callback_data='market')
    # builder.button(text=cancel_text, callback_data=PaymentsCallback(action='back_to', subject='all_goods'))
    builder.button(text=cancel_text,
                   callback_data=PaymentsCallback(action='show', subject='payment_ways', item=item, currency=currency))
    builder.adjust(1)
    return builder.as_markup()


sub_buying_failed_kb = {
    'en': InlineKeyboardMarkup(inline_keyboard =[
            [InlineKeyboardButton(text="Back", callback_data=PaymentsCallback(action='show', subject='all_goods', data='sub').pack())],
                ]
    ),
    'ru': InlineKeyboardMarkup(inline_keyboard =[
            [InlineKeyboardButton(text="Назад", callback_data=PaymentsCallback(action='show', subject='all_goods', data='sub').pack())],
                ]
        ),
}

async def get_pay_button(item: str, currency: str, method: str, lang='en'):
    buy_text = '➡ К оплате' if lang == 'ru' else '➡ Pay'

    builder = InlineKeyboardBuilder()

    builder.button(text=buy_text, callback_data=PaymentsCallback(
        action='pay', subject=method, item=item, currency=currency
    ))


    cancel_text = '⬅ Назад' if lang == 'ru' else '⬅ Back'

    # builder.button(text=cancel_text, callback_data='market')
    # builder.button(text=cancel_text, callback_data=PaymentsCallback(action='back_to', subject='all_goods'))
    builder.button(text=cancel_text,
                   callback_data=PaymentsCallback(action='show', subject='payment_methods', item=item, currency=currency))
    builder.adjust(1)
    return builder.as_markup()

async def get_cancel_payment_button(item, currency, lang: str='en'):

    builder = InlineKeyboardBuilder()
    cancel_text = '❌ Прервать оплату ❌' if lang =='ru' else '❌ Abort payment ❌'
    builder.button(text=cancel_text,
                   callback_data=PaymentsCallback(action='show',
                                                  subject='payment_ways',
                                                  item=item, currency=currency))
    builder.adjust(1)
    return builder.as_markup()

tinkoff_button = {
    'ru':  InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="↗  Быстрый перевод",
            web_app=WebAppInfo(url=shop_config.TINKOFF_PAY_URL)
        )
        ]
    ],
    ),
    'en': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="➡ Fast transfer",
            web_app=WebAppInfo(url=shop_config.TINKOFF_PAY_URL),
        )
        ]
    ],)
}



async def get_tinkoff_buy_button(item, currency, lang: str='en'):

    builder = InlineKeyboardBuilder().from_markup(tinkoff_button[lang])
    # builder = builder.from_markup(tinkoff_button[lang])

    # buy_text = '↗  Быстрый перевод' if lang == 'ru' else '➡ Fast transfer'
    # builder.button(text=buy_text,  url=shop_config.TINKOFF_PAY_URL, pay=True)
    cancel_text = '❌ Прервать оплату ❌' if lang =='ru' else '❌ Abort payment ❌'
    builder.button(text=cancel_text,
                   callback_data=PaymentsCallback(action='show', subject='payment_ways', item=item, currency=currency))
    # builder.button(text=cancel_text, callback_data=PaymentsCallback(action='show', subject='all_goods', data=item.split('-')[0]))
    builder.adjust(1)
    return builder.as_markup()


async def button_for_admin(payload: str, user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Confirm", callback_data=PaymentsCallback(action='approve', subject=str(user_id), data=payload))

    # builder.button(text=cancel_text, callback_data='market')
    # builder.button(text=cancel_text, callback_data=PaymentsCallback(action='back_to', subject='all_goods'))
    builder.button(text="Reject",
                   callback_data='cancel')
    builder.adjust(1)
    return builder.as_markup()