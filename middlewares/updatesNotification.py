from datetime import datetime
from typing import Callable, Dict, Any, Awaitable
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update


from processing import SQL_processingg as sqlp
from text_data.message_answers import answers_texts
from secret_data import TG_ADMIN_ID


class BotUpdatedMiddleware(BaseMiddleware):
    """
    Middleware to notice User about Bot was updated and ask user to restart Bot
    """
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        # Достаём данные из машины состояний
        fsm_data = data['state']
        try:
            lang = (await fsm_data.get_data())['language']
            return await handler(event, data)
        except KeyError:

            lang = event.from_user.language_code
            await fsm_data.update_data(language=lang)  # Удалить
            await event.answer(answers_texts['update_done'][lang].format(
                event.from_user.username
            ),
                # reply_markup=language_kb
            )

class BotUpdatingMiddleware(BaseMiddleware):
    """
    Middleware to say to user that the Bot is being updated right now
    If turned on, only Admin may use the Bot
    """
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        # Достаём данные из машины состояний
        fsm_data = data['state']
        try:
            lang = (await fsm_data.get_data())['language']
        except KeyError:
            lang = event.from_user.language_code
            await fsm_data.update_data(language=lang)
        if event.from_user.id == TG_ADMIN_ID:
            return await handler(event, data)
        else:
            await event.answer(answers_texts['update_is_going'][lang].format(
                event.from_user.username
            ),
            )