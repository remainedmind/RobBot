"""
Незарегистрированному пользователю будет доступна
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
from processing.SQL_processingg.SQL_high_level_processing import get_lang, get_user_info_quickly, get_balance_and_total
from processing.AccountProcessing import get_date_of_coins_updating
from text_data.message_answers import answers_texts
from text_data.user_settings import PROPERTIES_DEFAULT_VALUES
from keyboards.BasicKeyboards import more_coins_kb
from aiogram.dispatcher.flags import get_flag

from app.set_menu_commands import set_personal_menu_commands


class BalanceCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:

        # Достаём данные из машины состояний
        fsm_data = data['state']
        user_id = event.from_user.id
        try:
            chat_id = event.chat.id
        except AttributeError:
            chat_id = event.message.chat.id
        lang = (await fsm_data.get_data())['language']

        # Firstly, update all menu commands to the last version
        await set_personal_menu_commands(
            chat_id=chat_id, user_id=user_id, lang=lang, bot=data['bot']
        )




        user_info = await get_user_info_quickly(user_id)
        balance = user_info['balance']

        min_balance = get_flag(data, "coins_minimum")
        # print(min_balance, (min_balance == True), (balance > min_balance))
        # if min_balance is None:
        #     return await handler(event, data)
        if (min_balance is None) or balance > min_balance:
            return await handler(event, data)
        else:
            # lang = (await fsm_data.get_data())['language']
            type = 'zero' if min_balance == 0 else 'lack'
            update_date = await get_date_of_coins_updating(lang, user_info['expiry'])
            await event.answer(answers_texts['insufficient_balance'][type][lang].format(update_date),
                               reply_markup=more_coins_kb[lang])


