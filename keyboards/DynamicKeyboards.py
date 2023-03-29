from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton
from typing import Union, Tuple, List, Optional
from aiogram.filters.callback_data import CallbackData

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
# from textdata import properties
from text_data.user_settings import PROPERTIES, LANGUAGES, PROPERTIES_DEFAULT_VALUES


async def get_fererral_kb(lang='en', link=None) -> InlineKeyboardMarkup:
    """ Makes referral keyboard with user link"""
    if lang == 'ru':
        texts = ('↗️ Отправить ссылку другу', '⬅️ Назад')
    else:
        texts = ('↗️ Send link to friend', '⬅️ Back')
    builder = InlineKeyboardBuilder()
    builder.button(text=texts[0], switch_inline_query=link)
    builder.button(text=texts[1], callback_data='main')
    builder.adjust(1)
    return builder.as_markup()


class PropertiesCallback(CallbackData, prefix="property"):
    """
    Класс для обработки инлайн кнопок, связанных с пользовательскими
    настройками бота
    """
    param: str  # property name
    action: str  # show or switch
    value: Optional[int] = None
    data: Optional[str] = None


async def show_all_properties(info: dict, lang='en'):
    """
    Function to show all bot work params which can be edited by user
    """
    params = PROPERTIES[lang]

    builder = InlineKeyboardBuilder()
    switchers, choosers = params['switchers'], params['choosers']

    for key, data in switchers.items():
        try:
            param_value = info[key]
        except KeyError:
            # Default value for every parameter is in the end of tuple
            param_value = PROPERTIES_DEFAULT_VALUES[key]

        text_to_show = data['text']
        builder.button(
            text=text_to_show, callback_data=PropertiesCallback(param=key, value=param_value, action='show')
        )

    for key, data in choosers.items():
        try:
            param_value = info[key]
        except KeyError:
            param_value = PROPERTIES_DEFAULT_VALUES[key]
            # Default value for every parameter is in the end of tuple

            # param_value = data['property'][-1]
        #     value_to_show = all_values[default_value]
        #
        # text_to_show = data['text']
        # print(type(param_value), 'У НАС')
        text_to_show = data['text']
        builder.button(
            text=text_to_show, callback_data=PropertiesCallback(param=key, value=param_value, action='show')
        )

    builder.button(
        text= ("Язык" if lang == 'ru' else 'Language'),
        callback_data=PropertiesCallback(param='language', action='show', data=lang))
    # 'images_per_time': {
    #     'text': "Number of images",
    #     'property': "Always draw art"
    # }
    builder.button(
        text="🔙 " + ("Назад" if lang == 'ru' else 'Back'),
        callback_data="main")

    builder.adjust(1)
    return builder.as_markup()

is_property_active = {1: ' ✅', 0: ' ❎'}
is_option_active = {1: ' ✅', 0: ''}


async def get_property_status(param, value=None, lang='en'):
    """
    Function to show if specified property is acrive or not via button
    with emoji. When clicking the button, property status switch to
    opposite binary value
    """
    params = PROPERTIES[lang]
    # print("all", param, value)
    # print("мы тут", type(value))

    builder = InlineKeyboardBuilder()
    if param == 'language':
        for item in LANGUAGES.items():
            name = item[1]+is_option_active[item[0] == lang]
            builder.button(
                text=name,
                callback_data=PropertiesCallback(
                    param='language', action="set", data=item[0])
            )
        adjust = (1,)
    elif param in params['switchers']:

        property: str = params['switchers'][param]['property']

        # It's switching parameter (on or off)
        status = is_property_active[value]
        text_to_show = property + status

        builder.button(
            text=text_to_show, callback_data=PropertiesCallback(param=param, action="switch", value=int(value))
        )

        adjust = (1,)

    elif param in params['choosers']:

        property: dict = params['choosers'][param]
        options: dict = property['options']

        # It's a setting with multiple values
        for numeric_value, text_value in options.items():
            # print("Вот", type(numeric_value))
            status = is_option_active[value == numeric_value]
            text_to_show = text_value + status

            builder.button(
                text=text_to_show, callback_data=PropertiesCallback(param=param, action="set", value=numeric_value)
        )
        if param == 'temperature':
            adjust = (3, 3)
        else:
            adjust = (len(options), 1)

    builder.button(
        text="🔙 " + ("Назад" if lang == 'ru' else 'Back'),
        callback_data="settings")
    builder.adjust(*adjust)
    return builder.as_markup()
