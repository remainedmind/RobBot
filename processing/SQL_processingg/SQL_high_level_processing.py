"""
Module fot SQ3Lite processing, which supports asynchronous work.
As we pass async. connection to our read/write functions from above
(means from main script), we don't need aiosqlite module right here.

Модуль для работы с SQLite3
Функции создания таблицы и извлечения списка столбцов
сихронные, а функции чтения и записи, работающие постоянно,
поддерживают асинхронную работу: асинхронное соединение CON
передаются из главного скрипта, так что импортировать
aiosqlite сюда нам не трубется
"""

import aiosqlite
import asyncio
import sqlite3
from const import DATABASE, TABLE, DEFAULT_BALANCE, INSTANT_REFERRAL_REWARD, UPDATE_TIME
from datetime import datetime
from processing.SQL_processingg import SQL_low_level_processing as low_level_sql

from processing.timeProcessing import set_expiry_date


async def add_new_user(id: int, nickname: str, lang: str, now: datetime):
    """
    Function to add new user
    :param id:
    :param nickname:
    :param lang:
    :param now: UTC time
    :return:
    """
    expiry_date = await set_expiry_date(date=now, extra_time=UPDATE_TIME)
    added = await low_level_sql.add_user((id, nickname, expiry_date, lang))
    if added:
        return True
    else:
        # If user just restarts the bot, we update the data
        process = await low_level_sql.update_info(
            ('nickname', 'language'), (nickname, lang), id
        )
        if process:
            print('change data')


async def get_lang(id):
    """
    Fast way to check whether we have a person in our DB or no
    """
    info = await low_level_sql.get_user_info(id=id)
    if not info:  # Человека нет в БД
        return False
    lang = info['language']
    return lang


async def get_customers_data(method: str = 'data', con: aiosqlite.Connection = None):
    """
    Get all info about user
    """
    info = await low_level_sql.get_user_info(method=method, con=con)
    if info:
        return info
    else:
        return False


async def get_user_info_quickly(id):
    """
    Get all info about user
    """
    info = await low_level_sql.get_user_info(id=id)
    if info:
        return info
    else:
        return False


async def get_balance_and_total(id) -> tuple[int|None, int|None]:
    """
    Get all info about user
    """
    info = await low_level_sql.get_user_info(id=id)
    if info:
        return info['balance'], info['total']
    else:
        return None, None


async def get_info_by_nickname(username):
    """
    Быстрый способ проверить, есть ли человек в БД
    """
    info = await low_level_sql.get_user_info(nickname=username)
    if info:
        return info
    else:
        return False


async def check_for_premium(id) -> str:
    """
    Быстрый способ проверить, есть ли человек в БД
    """
    info = await low_level_sql.get_user_info(id=id)
    if info:
        return info['status']
    return False


async def change_coins_balance(id, charge, method='take_for_chatting', date: datetime|None=None, con: aiosqlite.Connection|None=None):
    """
    :param con: SQL connection
    """
    balance, total = await get_balance_and_total(id)
    columns = []
    values = []
    if method == 'take_for_chatting':
        if balance > charge:
            balance -= charge
        else:  # Отрицательный баланс обнуляем
            balance = 0

        total += charge
    elif method == 'buy':
        if balance > charge:
            balance -= charge
        else:  # Отрицательный баланс обнуляем
            return False

        total += charge
    elif method == 'update':
        date = await set_expiry_date(date=date, extra_time=UPDATE_TIME)
        columns.append('expiry')
        values.append(date)
        # Here we don't add coins - we replace it
        balance = charge
    else:  # elif method == 'put':
        balance += charge
    columns.append('balance'),  columns.append('total')
    values.append(balance), values.append(total)
    process = await low_level_sql.update_info(
        columns, values, id, con
    )
    if process:
        return True
    else: return False




async def set_new_status(user_id: int, new_status: str, now: datetime | None = None, period: dict |None = None, con: aiosqlite.Connection|None=None):
    """
    Changing the user status
    """
    if new_status == 'premium':
        prem_expiry_date = await set_expiry_date(date=now, extra_time=period)
        # We also reset coins update date
        coins_update =  await set_expiry_date(date=now, extra_time=dict(seconds=20))
    else:
        prem_expiry_date = None


    process = await low_level_sql.update_info(
        ('status', 'prem_expires'), (new_status, prem_expiry_date), user_id, con
    )
    if process:
        return True
    else: return False


async def add_referral(referrer_id, new_client_id, con: aiosqlite.Connection|None=None):
    """ Награждаем пользователя за реферала и вносим реферала в базу"""
    referrer_info = await low_level_sql.get_user_info(id=referrer_id)
    if not referrer_info:
        return None
    referrer_refs = referrer_info['referrals']
    referrer_status = referrer_info['status']
    referrer_reward = INSTANT_REFERRAL_REWARD


    if all(
            (
            # We add referrer id to new user info
            await low_level_sql.update_info(('referrer',), (referrer_id,), new_client_id, con),

        # We reward our referrer
            await low_level_sql.update_info(('referrals',), (referrer_refs+1,), referrer_id, con),
            await change_coins_balance(id=referrer_id, charge=referrer_reward, method='put')
            )
    ):
        return referrer_reward
    else:
        print("nonr")
        return None
# main()


async def add_new_payment(query_id,
                          user_id, username, first_name, second_name,
                          currency, price, payload) -> bool:
    """
    Function to add new user
    :param id:
    :param nickname:
    :param lang:
    :param now: UTC time
    :return:
    """
    # date = await set_expiry_date(now)
    added = await low_level_sql.add_payment(
        (query_id, user_id, username, first_name, second_name, currency, price,
         payload,
         # date
         )
    )
    if added:
        return True
    else:
        return False


async def confirm_payment(user_id, payload, now: datetime) -> bool:
    """
    payload: includes random string key which help to find record
    """
    date = now.strftime("%Y.%m.%d %H:%M")
    confirmed = await low_level_sql.update_payment(user_id, payload, date)
    if confirmed:
        return True
    else:
        return False




async def shutdown_aiosqlite():
    low_level_sql.shutdown_connection()




