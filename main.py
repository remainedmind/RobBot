import asyncio
import logging


from aiogram import Bot, Dispatcher
from aiogram.dispatcher.event.event import EventObserver
from aiogram.filters import invert_f
from aiogram.fsm.storage.redis import RedisStorage
from secret_data import TG_TOKEN, TG_ADMIN_ID
from handlers import AdminCommands, BasicPublicCommands, RestMessagesHandlers, BotBlockingHandler
from payments.pay_handlers import router as pay_router
from handlers.callbacks import BasicQueries, CasinoQueries, SettingsQueries
from handlers.hard_part import conversationHandlers, conversationCallbacks

from app.finite_state_machine import UserStates

import os




from middlewares.RegistrationCheck import AccessCheckMiddleware


from processing.SQL_processingg.SQL_low_level_processing import create_table, collect_columns, open_connection
from app.set_menu_commands import set_default_command_menu
from app.coins_updating import behind_loop
from processing.SQL_processingg.SQL_low_level_processing import shutdown_connection

# def shutdown_redis()

async def main() -> None:
    # redis_con = Redis(host="127.0.0.1", port=6379)
    # storage = RedisStorage(redis_con)
    redistorage = RedisStorage.from_url('redis://localhost:6379/0')


    dp = Dispatcher(storage=redistorage)
    # dp = Dispatcher()

    # When shutdown, we close SQL and Redis connections
    observer = EventObserver()
    observer.register(shutdown_connection)
    observer.register(redistorage.close)

    dp.include_routers(
        BotBlockingHandler.router,
        pay_router,
        BasicPublicCommands.router,
        AdminCommands.router,
        conversationHandlers.router,
        conversationCallbacks.router,
        RestMessagesHandlers.router,
        BasicQueries.router,
        SettingsQueries.router,
        CasinoQueries.router
    )

    dp.message.middleware(AccessCheckMiddleware())
    dp.callback_query.middleware(AccessCheckMiddleware())


    bot = Bot(TG_TOKEN, parse_mode="HTML")


    await set_default_command_menu(bot)

    loop = asyncio.get_event_loop()
    loop.create_task(behind_loop(bot))

    # And the run events dispatching
    await dp.start_polling(bot, skip_updates=True)











if __name__ == "__main__":
    # filename = "/foo/bar/baz.txt"
    os.makedirs(os.getcwd()+'/voices', exist_ok=True)
    create_table()
    collect_columns()



    logging.basicConfig(level=logging.INFO)
    # По умолчанию на уровне INGO логгер отображает в том числе
    # новые сообщения Боту, т.е. обновления. Нам это не интересно,
    # поэтому откроем:
    # module dispatcher -> Class Dispatcher -> func feed_update
    # и сменим уровень логирования с loggers.event.info на
    # loggers.event.debug. Теперь уведомления об обновлениях получать
    # не будем
    asyncio.run(main())
