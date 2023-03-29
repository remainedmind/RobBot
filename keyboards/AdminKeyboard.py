from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Union, Tuple, List, Optional, Any
from aiogram.filters.callback_data import CallbackData

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from secret_data import TG_ADMIN_ID




class AdminCallbacks(CallbackData, prefix="admin_panel"):
    """
    Класс для работы с контектом во время переписки с ботом:
    начало ведения диалога, сброс, выключение контекста
    """
    user_id: Optional[int]
    status: Optional[str]  # premium | user
    action: str | int
    data: Optional[str | int]







async def build_keyboard(user_id=TG_ADMIN_ID, action=None, status=None, data=None):
    """
    Function to show if specified property is acrive or not via button
    with emoji. When clicking the button, property status switch to
    opposite binary value
    """

    builder = InlineKeyboardBuilder()
    if action == 'manage':
        builder.button(text="Change balance", callback_data=AdminCallbacks(user_id=user_id, status=status, action='change', data='balance'))
        builder.button(text="Change status", callback_data=AdminCallbacks(user_id=user_id, status=status, action='change', data='status'))
    elif action == 'change':
        if data == 'status':
            new_status = "premium" if status == 'user' else 'user'
            builder.button(
                text="Set: {}".format(new_status),
                callback_data=AdminCallbacks(user_id=user_id, status=new_status, action='confirm', data='status'))
    elif action == 'send_spam':
        builder.button(
            text="RU",
            callback_data=AdminCallbacks(action='confirm_spam', data='ru'))
        builder.button(
            text="EN",
            callback_data=AdminCallbacks(action='confirm_spam', data='en'))
        builder.button(
            text="Everyone",
            callback_data=AdminCallbacks(action='confirm_spam', data='all'))


    builder.button(text="Cancel", callback_data=AdminCallbacks(action='cancel'))
    builder.adjust(1)
    return builder.as_markup()

