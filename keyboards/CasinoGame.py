from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Union, Tuple, List, Optional
from aiogram.filters.callback_data import CallbackData

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from text_data.user_settings import SLOT_MACHINE_BETS

class CasinoCallback(CallbackData, prefix="casino"):
    """
    """
    action: str  # play, rules
    value: Optional[int]

casino_start_kb = {
    'en':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="➡ Play", callback_data=CasinoCallback(action='play').pack())],
                [InlineKeyboardButton(text="💰 Bet size", callback_data=CasinoCallback(action='show_settings').pack())],
                [InlineKeyboardButton(text="📋 Game rules", callback_data=CasinoCallback(action='show_rules').pack())],
                [InlineKeyboardButton(text="⬅ Back", callback_data="main")]
            ]
        ),
    'ru':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="➡ Играть", callback_data=CasinoCallback(action='play').pack())],
                [InlineKeyboardButton(text="💰 Ставка", callback_data=CasinoCallback(action='show_settings').pack())],
                [InlineKeyboardButton(text="📋 Правила игры", callback_data=CasinoCallback(action='show_rules').pack())],
                [InlineKeyboardButton(text="⬅ Назад", callback_data="main")]
            ]
        )
}


casino_play_kb = {
        'en': InlineKeyboardMarkup(inline_keyboard = [
                [InlineKeyboardButton(text="🔄 Again", callback_data=CasinoCallback(action='play').pack())],
                [InlineKeyboardButton(text="🔚 Finish", callback_data="casino")]
            ],
        ),
        'ru': InlineKeyboardMarkup(inline_keyboard = [
                [InlineKeyboardButton(text="🔄 Ещё раз", callback_data=CasinoCallback(action='play').pack())],
                [InlineKeyboardButton(text="🔚 Закончить", callback_data="casino")]
            ]
    )
}

casino_help_kb = {
    'en': InlineKeyboardMarkup(inline_keyboard = [
                [InlineKeyboardButton(text="🔙 Back", callback_data="casino")]
            ]
    ),
    'ru': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="casino")]
    ]
    ),
}



is_option_active = {True: '  ✅', False: ''}

async def get_bet_settings(value: int, lang='en'):
    """
    Function to show if specified property is acrive or not via button
    with emoji. When clicking the button, property status switch to
    opposite binary value
    """


    builder = InlineKeyboardBuilder()

    for bet in SLOT_MACHINE_BETS:
        name = str(bet)+is_option_active[bet == value]
        builder.button(
            text=name,
            callback_data=CasinoCallback(
                action="set_bet", value=bet)
        )
    builder.button(
        text="🔙 " + ("Назад" if lang == 'ru' else 'Back'),
        # callback_data=CasinoCallback(action='set_bet', param='sm_bet').pack())
        callback_data = 'casino')
    builder.adjust(len(SLOT_MACHINE_BETS), 1)
    return builder.as_markup()



