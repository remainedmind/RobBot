from collections import  OrderedDict
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update

from aiogram.dispatcher.flags import get_flag

from aiogram.types import Message

from processing.SQL_processingg.SQL_high_level_processing import check_for_premium




from text_data.message_answers import answers_texts as ma_texts

THROTTLED_USERS_LIMIT = 50
PREMIUM_SPEED_INCREASE = 5
active_users = OrderedDict()


class ThrottlingMiddleware(BaseMiddleware):
    """
    As named, Middleware for Throttling. As the easiest way, dict is used.
    """
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        throttling_delay = get_flag(data, "throttling")  # value in seconds

        # If we send command without param, we shouldn't use throttling
        text = data['event_update'].message.text
        user_id = event.from_user.id

        try:
            # We check, if user passes empty command. In this case we don't
            # need to use throttling, because user need to pass args next step
            command = data['command']  # -> place for KeyError
            if text[1:] == command.command:  # -> another place is in slicing
                # Then we cancel trottling
                return await handler(event, data)
        except KeyError:
            # in case we send voice message, we don't have command field
            pass
        if throttling_delay:
            # print(event.date.now() - event.date.now())
            if not user_id in active_users.keys():
                active_users[user_id] = event.date.now()
                await handler(event, data)
                if len(active_users) > THROTTLED_USERS_LIMIT:
                    # Удаляем старые данные
                    active_users.popitem(last=False)
                # return await handler(event, data)
                # return result
            else:
                delta = (event.date.now() - active_users[user_id]).total_seconds()
                user_status = await check_for_premium(user_id)

                if user_status == 'premium':
                    # We decrease delay for PREMIUM
                    throttling_delay /= PREMIUM_SPEED_INCREASE

                if delta > throttling_delay:
                    active_users[event.chat.id] = event.date.now()
                    return await handler(event, data)

                else:
                    # Show to user how many seconds he has to wait
                    fsm_data = data['state']
                    info = (await fsm_data.get_data())

                    lang = info['language']
                    # Or we can use:
                    # lang = event.from_user.language_code
                    return await event.answer(
                        ma_texts['throttling'][lang].format(
                            round(throttling_delay - delta, 1)
                        )
                    )
        else:
            return await handler(event, data)
