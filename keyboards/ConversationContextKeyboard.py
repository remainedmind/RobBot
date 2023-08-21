from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Union, Tuple, List
from aiogram.filters.callback_data import CallbackData

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# async def Chat() -> dict:
#     dialogue = {}
#     dialogue['chat'] = []
#     dialogue['active'] = False
#     return dialogue
#
#
# async def start_chat(dialogue):
#     dialogue['chat'] = []
#     dialogue['active'] = True
#     return dialogue
#
# async def add_user_message(dialogue, text):
#     dialogue['chat'].append({"role": "user", "content": text})
#     return dialogue
#
# async def add_bot_message(dialogue, text):
#     dialogue['chat'].append({"role": "assistant", "content": text})
#     return dialogue
#
# async def reset_chat(dialogue):
#     dialogue['chat'].clear()
#     return dialogue
#
# async def stop_chat(dialogue):
#     dialogue['chat'].clear()
#     dialogue['active'] = False
#     return dialogue
#
# async def remove_old_messages(dialogue):
#     # Delete last messages because of dialogue is exceeding GPT limit
#     dialogue['chat'].pop(0)
#
#

#
class Chat():
    """
    Класс, предназначенный для ведения диалога с GPT-моделью.
    Собирает список из сообщений от двух сторон.
    """
    def __init__(self,):
        self.chat = []
        self.active = False  # Будем ли мы запоминать контекст

    async def start_chat(self):
        self.chat.clear()
        self.active = True

    async def add_user_message(self, text):
        self.chat.append({"role": "user", "content": text})

    async def add_bot_message(self, text):
        self.chat.append({"role": "assistant", "content": text})

    async def reset_chat(self):
        self.chat.clear()

    async def stop_chat(self):
        self.chat.clear()
        self.active = False

    async def remove_old_messages(self):
        # Delete last messages because of dialogue is exceeding GPT limit
        self.chat.pop(0)




class ConversationCallback(CallbackData, prefix="conversation"):
    """
    Класс для работы с контектом во время переписки с ботом:
    начало ведения диалога, сброс, выключение контекста
    """
    data: str  # keep main param
    action: str

start_kb = {
    'en':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Start dialogue", callback_data=ConversationCallback(data='dialogue', action='start').pack())],
            ]
        ),
    'ru':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Начать диалог", callback_data=ConversationCallback(data='dialogue', action='start').pack())],
            ]
        )
}

reset_kb = {
    'en':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Reset dialogue", callback_data=ConversationCallback(data='dialogue', action='reset').pack())],
            ]
        ),
    'ru':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Сбросить диалог", callback_data=ConversationCallback(data='dialogue', action='reset').pack())],
            ]
        )
}

stop_kb = {
    'en':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Stop dialogue", callback_data=ConversationCallback(data='dialogue', action='stop').pack())],
            ]
        ),
    'ru':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Завершить диалог", callback_data=ConversationCallback(data='dialogue', action='stop').pack())],
            ]
        )
}

reset_and_stop_kb = {
    'en':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Reset dialogue", callback_data=ConversationCallback(data='dialogue', action='reset').pack()), InlineKeyboardButton(text="Stop dialogue", callback_data=ConversationCallback(data='dialogue', action='stop').pack())],
            ]
        ),
    'ru':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Сбросить диалог", callback_data=ConversationCallback(data='dialogue', action='reset').pack()), InlineKeyboardButton(text="Завершить диалог", callback_data=ConversationCallback(data='dialogue', action='stop').pack())],
            ]
        )
}

voice_kb = {
    'en':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Yeah, answer that", callback_data=ConversationCallback(data='voice', action='ask').pack())],
                [InlineKeyboardButton(text="No, forget it", callback_data=ConversationCallback(data='voice', action='pass').pack())]
            ]
        ),
    'ru':
        InlineKeyboardMarkup(inline_keyboard =[
                [InlineKeyboardButton(text="Да, ответь", callback_data=ConversationCallback(data='voice', action='ask').pack()),
                InlineKeyboardButton(text="Нет, забудь", callback_data=ConversationCallback(data='voice', action='pass').pack())],
            ]
        )
}
