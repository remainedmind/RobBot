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
from constants.const import DATABASE, TABLE, DEFAULT_BALANCE



def create_table():
    """ Функция для создания таблицы при запуске бота """
    db  = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    sql = ("""
        CREATE TABLE IF NOT EXISTS {}(
        id INTEGER PRIMARY KEY, 
        nickname TEXT,
        status TEXT DEFAULT user,  
        expiry TEXT DEFAULT NULL,
        balance INTEGER DEFAULT {},
        referrals INTEGER DEFAULT 0,
        language TEXT DEFAULT en,
        total INTEGER DEFAULT 0,
        referrer INTEGER,
        prem_expires TEXT)""".format(
        TABLE, DEFAULT_BALANCE['user']['general']
        )
    )
    cursor.execute(sql)
    db.commit()

    sql = ("""
        CREATE TABLE IF NOT EXISTS payments(
        query_id TEXT,
        user_id INTEGER, 
        nickname TEXT,
        first_name TEXT,
        second_name TEXT,
        currency TEXT,
        price INTEGER,
        payload TEXT PRIMARY KEY,
        date TEXT,
        success INTEGER DEFAULT 0
        )"""
    )
    cursor.execute(sql)
    db.commit()

    db.close()


COLUMN_NAMES = []

def collect_columns():
    db  = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {TABLE} ;")

        # Метод description возвращает кортежи, в которых первый
        # элемент - название столбца, остальное - None
    [
        COLUMN_NAMES.append(d[0]) for d in cursor.description
    ]
    db.close()


# CONNECTION: aiosqlite.Connection
# global CONNECTION
# CONNECTION = 1

READ_CONNECTION: aiosqlite.Connection  # Connection only for reading
WRITE_CONNECTION: aiosqlite.Connection


async def open_connection() -> None:
    """ Open the connection with Database"""

    global READ_CONNECTION
    global WRITE_CONNECTION
    READ_CONNECTION = await aiosqlite.connect(DATABASE)
    WRITE_CONNECTION = await aiosqlite.connect(DATABASE)

asyncio.run(open_connection())

async def add_user(values: tuple, con=WRITE_CONNECTION):
    """
    Функция для добавления нового пользователя
    :param con: active connection
    :param values: (id value, nickname text, expiry, lang)
    :return:
    """
    # async with aiosqlite.connect('CUSTOMERS.db') as con:

    async with con.cursor() as cursor:
        try:
            sql = f"""INSERT INTO {TABLE} (id, nickname, expiry, language) VALUES(?, ?, ?, ?);"""
            await cursor.execute(sql, values)
            await con.commit()
            return True  # Успешно добавили пользователя
        except sqlite3.IntegrityError:
            return False
        except:
            return None


async def update_info(columns, values, id, con: aiosqlite.Connection|None=None):
    """
    Функция для обновления пользовательских данных.
    :param id: user's id
    :param con: async connection
    :param columns: tuple of names
    :param values: tuple of values
    :return: True is success
    """
    if not con:
        con = WRITE_CONNECTION
    async with con.cursor() as cursor:
        # Для SQL-запросов нам нужно получить строки из кортежей
        # Во избежание SQL-инъекций мы используем ?
        gaps = ', '.join([f"{col} = ?" for col in columns])
        try:
            sql = f"""UPDATE {TABLE} SET {gaps}  WHERE id={id};"""
            await cursor.execute(sql, values)  # inserting data from values tuple
            await con.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except:
            raise



async def get_user_info(id=None, nickname=None, method=None, con: aiosqlite.Connection|None=None):
    """
    Get all info in two ways:
    1) info about 1 person - to change it (e.x. charging balance)
    2) info about all users - to update each in while loop or to learn users number
    :param con: async connection
    :param id: user id if we prefer 1 way
    :param nickname: alternative way to find a user
    :param method: way we'd like to use
    :return: list of tuples (all users) or dict (one user)
    """
    if not con:
        con = READ_CONNECTION
    async with con.cursor() as cursor:
        if any((id, nickname)):  # Достаём данные об одном человеке
            if id:
                col = 'id'
                val = id
            else:
                col = 'nickname'
                val = nickname
            # col = 'id' if id else 'nickname'
            # val = id or nickname
            try:
                await cursor.execute(f"SELECT * FROM {TABLE} WHERE {col} = ?;", (val, ))
                # aiosqlite поддерживает только метод fetchall, так что мы
                # получим список из одного элемента - кортежа. Сделаем срез.
                info = (await cursor.fetchall())[0]
                return (
                    # Формируем словарь
                    {
                        k: v for k, v in zip(COLUMN_NAMES, info)
                    }
                )
            except IndexError:  # Человека нет в БД - не смогли сделать срез
                # raise
                return False
            except:
                # raise
                return False
        else:
            if method == 'data':
                # Достаём всю информацию
                await cursor.execute(f"SELECT * FROM {TABLE};")
            elif method == 'amount':
                # Достаём количество пользоваетелей
                await cursor.execute(f"SELECT count(*) FROM {TABLE};")
            # Возвращаем данные
            return (await cursor.fetchall())



async def add_payment(values: tuple, con=WRITE_CONNECTION):
    """
    Функция для добавления нового пользователя
    :param con: active connection
    :param values: (id value, nickname text, expiry, lang)
    :return:
    """

    # query_id, user_id,first_name,second_name, currency, price, coins, date
    async with con.cursor() as cursor:
        try:
            sql = f"""INSERT INTO payments (query_id, user_id, nickname,
            first_name,second_name, currency, price, payload) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""
            await cursor.execute(sql, values)
            await con.commit()
            return True  # Успешно добавили пользователя
        except sqlite3.IntegrityError:
            return False
        except:
            return None


async def update_payment(user_id, payload, date: str, con=WRITE_CONNECTION):
    """
    Функция для добавления нового пользователя
    :param con: active connection
    :param values: (id value, nickname text, expiry, lang)
    :return:
    """

    # query_id, user_id,first_name,second_name, currency, price, coins, date
    async with con.cursor() as cursor:
        try:
            sql = f"""UPDATE payments SET date=?, success=1 WHERE user_id=? AND payload=?;"""
            await cursor.execute(sql, (date, user_id, payload))
            await con.commit()
            return True  # Успешно добавили пользователя
        except sqlite3.IntegrityError:
            return False
        except:
            return None




async def async_main():
    async with aiosqlite.connect('../'+DATABASE) as con:
        async with con.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM payments WHERE id=406570178;")
            print(await cursor.fetchall())



def shutdown_connection():
    """ End of work"""
    READ_CONNECTION.close()
    WRITE_CONNECTION.close()

if __name__ == '__main__':
    asyncio.run(async_main())






