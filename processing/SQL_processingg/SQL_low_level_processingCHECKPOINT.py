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
from const import DATABASE, TABLE, DEFAULT_BALANCE



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
        language TEXT DEFAULT ru,
        total INTEGER DEFAULT 0,
        referrer INTEGER,
        prem_expires TEXT)""".format(
        TABLE, DEFAULT_BALANCE['user']['general']
        )
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



async def add_user(con, values):
    """
    Функция для добавления нового пользователя
    :param db:
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


async def update_info(con, columns, values, id):
    """
    Функция для обновления пользовательских данных.
    :param id: user's id
    :param con: async connection
    :param columns: tuple of names
    :param values: tuple of values
    :return: True is success
    """
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



async def get_user_info(con, id=None, nickname=None, method=None):
    """
    Get all info it two ways:
    1) info about 1 person - to change it (e.x. charging balance)
    2) info about all users - to update each in while loop or to learn users number
    :param con: async connection
    :param id: user id if we prefer 1 way
    :param nickname: alternative way to find a user
    :param method: way we'd like to use
    :return: list of tuples (all users) or dict (one user)
    """
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


async def get_lang(id):
    """
    Быстрый способ проверить, есть ли человек в БД
    """
    async with aiosqlite.connect(DATABASE) as con:
        info = await get_user_info(con, id=id)
        if not info:  # Человека нет в БД
            return False
        lang = info['language']
    return lang

async def get_user_info_quickly(id):
    """
    Быстрый способ проверить, есть ли человек в БД
    """
    async with aiosqlite.connect(DATABASE) as con:
        info = await get_user_info(con, id=id)
        if info:
            return info
        else:
            return False

async def get_id_by_nickname(username):
    """
    Быстрый способ проверить, есть ли человек в БД
    """
    async with aiosqlite.connect(DATABASE) as con:
        info = await get_user_info(con, nickname=username)
        if info:
            return info['id']
        else:
            return False



async def async_main():
    async with aiosqlite.connect(DATABASE) as con:
        async with con.cursor() as cursor:
            await cursor.execute(f"SELECT count(*) FROM {TABLE};")
            print(await cursor.fetchall())

# main()

if __name__ == '__main__':
    asyncio.run(async_main())






