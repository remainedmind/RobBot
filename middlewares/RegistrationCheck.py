"""
Незарегестрированному пользователю будет доступна
только команда /start. В качестве проверки используется фукнция,
которая достаёт из БД установленный язык.
Сразу после регистрации устанавливаются все дефолтные настройки
"""



from datetime import datetime
import aiosqlite
from typing import Callable, Dict, Any, Awaitable
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update


# from processing.SQL_processingg.SQL_low_level_processing import get_lang
from processing.SQL_processingg.SQL_high_level_processing import get_lang
from text_data.message_answers import answers_texts as ma_texts
from text_data.user_settings import PROPERTIES_DEFAULT_VALUES



class AccessCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:

        try:
            user_id = event.from_user.id
            chat_id = event.chat.id
        except:
            pass

        # Достаём данные из машины состояний
        fsm_data = data['state']
        try:
            lang = (await fsm_data.get_data())['language']
            return await handler(event, data)
        except KeyError:
            # GO to Database
            lang = await get_lang(user_id)
            if lang:  # User exists
                await fsm_data.update_data(language=lang)
                await handler(event, data)
                # for property, d_value in PROPERTIES_DEFAULT_VALUES.item():

                # Set default values
                await fsm_data.update_data(**PROPERTIES_DEFAULT_VALUES)
            else:  # New user
                try:
                    command = data['command']  # -> place for KeyError
                    if command.command == 'start':  # the only message we accept
                        return await handler(event, data)
                    else:
                        raise KeyError  # we won't call the handler
                except KeyError:
                    # in case we send voice message, we don't have command field
                    lang = event.from_user.language_code
                    try:
                        _  = event.message_id
                        send = event.answer
                    except AttributeError:
                        _ = event.id  # Check for attribute existing
                        send = event.message.answer


                    await send(ma_texts['start']['new_user'][lang].format(
                        event.from_user.first_name
                    )
                    )
