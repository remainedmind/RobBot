from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Union, Tuple, List, Optional
from aiogram.filters.callback_data import CallbackData

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



class FeedbackCallback(CallbackData, prefix="feedback"):
    """
    """
    action: str

confirm_feedback_kb = {
    'en':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="✔ Confirm", callback_data=FeedbackCallback(action='send_to_admin').pack()),
                InlineKeyboardButton(text="✖ Cancel", callback_data=FeedbackCallback(action="cancel").pack())]
            ]
        ),
    'ru':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="✔ Подтвердить", callback_data=FeedbackCallback(action='send_to_admin').pack()),
                InlineKeyboardButton(text="✖ Отменить", callback_data=FeedbackCallback(action="cancel").pack())]
            ]
        )
}

confirm_answer_kb = InlineKeyboardMarkup(
    inline_keyboard =[
                [InlineKeyboardButton(text="✔ Confirm", callback_data=FeedbackCallback(action='send_to_user').pack()),
                InlineKeyboardButton(text="✖ Cancel", callback_data=FeedbackCallback(action="cancel").pack())]
            ]
)
# print(confirm_answer_kb)


