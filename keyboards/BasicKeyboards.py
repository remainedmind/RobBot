from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.callback_game import CallbackGame
from typing import Union, Tuple, List


from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup,
                           KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from secret_data import TG_RU_CHANNEL_LINK


# Клавиатура[строка[кнопка[text & data], ...], ...]
def get_keyboard(
        # buttons: List[List[Tuple[str, ..., Union[str, int],]]],
        buttons,
        langs: Tuple[str, ...]) -> dict[str, list | InlineKeyboardMarkup]:
    """
    Функция для создания клавиатуры
    :param buttons: двумерный массив кортежей из двух элементов:
    название кнопки и callback значение. Структура массива
    полностью повторяет структуру клавиатуры, которая будет
    возвращена
    :return: словарь, в котором ключи - поддерживаемые языки, а
    значения - соответсвующие клавиатуры
    """

    boards = {}
    for i, lang in enumerate(langs):
        boards[lang] = []
        for row in buttons:
            layer_buts = []
            for but in row:
                layer_buts.append(InlineKeyboardButton(text=but[i], callback_data=but[-1]))
            boards[lang].append(layer_buts)
        boards[lang] = InlineKeyboardMarkup(inline_keyboard = boards[lang])
    del layer_buts
    return boards


start_kb = get_keyboard(
    [
        [('Поехали', "Let's start", 'ready')],
    ], langs=('ru', 'en')
)


main_page_kb = get_keyboard(
    [
        [
            ('🤖 Мой аккаунт', '🤖 My account', 'account'),
            ('💳 Покупки', '💳 Buy', 'market')
        ],
        [
            ('📋 Справка', '📋 Learn', 'help'),
            ('🎰 Казино', '🎰 Casino', 'casino')
        ],
        [
            ('⚙ Настройки', '⚙ Settings', 'settings'),
            ('🎣 Привести друга', '🎣 Invite friend','referral')
         ]
    ], langs=('ru', 'en')
)

more_coins_kb = get_keyboard(
    [
        [
            ('🔎 Больше монет', '🔎 More coins', 'market'),
         ]
    ], langs=('ru', 'en')
)

account_from_command_kb = get_keyboard(
    [
        [
            ('🔎 Больше монет', '🔎 More coins', 'market'),
         ]
    ], langs=('ru', 'en')
)

account_from_menu_kb = get_keyboard(
    [
        [
            ('🔎 Больше монет', '🔎 More coins', 'market'),
            ('🔙 Назад', '🔙 Back', 'main')
         ]
    ], langs=('ru', 'en')
)

# language_kb = InlineKeyboardMarkup(
#     inline_keyboard = [
#         [InlineKeyboardButton(text="English", callback_data="en"),
#          InlineKeyboardButton(text="Русский", callback_data="ru")]
#     ]
# )



cancel_kb = get_keyboard(
    [
        [
            ('✖ Отменить', '✖ Cancel', 'cancel'),
         ]
    ], langs=('ru', 'en')
)


help_kb = get_keyboard(
    [
        [(
            '⁉ Зачем ограничения в виде монет?', '⁉ Why I have limitations in the form of coins?', 'restriction_reason'
        )],
        [('🔙 Назад', '🔙 Back', 'main')],
    ], langs=('ru', 'en')
)

back_to_main_kb = get_keyboard(
    [
        [('🔙 Назад', '🔙 Back', 'main')],
    ], langs=('ru', 'en')
)

back_and_cancel_kb = get_keyboard(
    [
        [('🔙 Назад', '🔙 Back', 'back')],
        [('✖ Отменить', '✖ Cancel', 'cancel')],
    ], langs=('ru', 'en')
)

confirm_feedback_kb = get_keyboard(
    [
        [('✔ Подтвердить', '✔ Confirm', 'send_feedback')],
        [('✖ Отменить', '✖ Cancel', 'cancel')],
    ], langs=('ru', 'en')
)


subscribe_to_ru_channel_kb = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text="Подписаться на новостной канал", url=TG_RU_CHANNEL_LINK)]
    ]
)