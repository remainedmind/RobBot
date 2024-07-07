import os
# import sys
# sys.path.append(os.getcwd())


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

from web.web_app import run_web

from middlewares.RegistrationCheck import AccessCheckMiddleware

from processing.SQL_processingg.SQL_low_level_processing import create_table, collect_columns, open_connection
from app.set_menu_commands import set_default_command_menu
from app.coins_updating import behind_loop, update_users_coins
from processing.SQL_processingg.SQL_low_level_processing import shutdown_connection

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def main() -> None:
    # To store states, we use Redis (while development, it's off - uncomment for production)
    # redistorage = RedisStorage.from_url('redis://localhost:6379/0')

    # dp = Dispatcher(storage=redistorage)
    dp = Dispatcher()

    # When shutdown, we close SQL and Redis connections
    observer = EventObserver()
    observer.register(shutdown_connection)
    # observer.register(redistorage.close)  # To shut down

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

    # scheduler.add_job(
    #     update_users_coins, 'interval', hours=3,
    #     kwargs={"bot": bot,}
    # )

    # We enable coins updating at every 2 days
    scheduler.add_job(
        update_users_coins, 'cron',
        day=2,
        # second=12,
        kwargs={"bot": bot, }
    )
    scheduler.start()

    await set_default_command_menu(bot)

    loop = asyncio.get_event_loop()
    # loop.create_task(behind_loop(bot))
    # loop.create_task(run_web())
    # await run_web()

    # And the run events dispatching
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    # filename = "/foo/bar/baz.txt"
    os.makedirs(os.getcwd() + '/voices', exist_ok=True)
    create_table()
    collect_columns()

    logging.basicConfig(level=logging.INFO,
                        filename='bot_logs.txt',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                        )
    # По умолчанию на уровне INGO логгер отображает в том числе
    # новые сообщения Боту, т.е. обновления. Нам это не интересно,
    # поэтому откроем:
    # module dispatcher -> Class Dispatcher -> func feed_update
    # и сменим уровень логирования с loggers.event.info на
    # loggers.event.debug. Теперь уведомления об обновлениях получать
    # не будем
    asyncio.run(main())
