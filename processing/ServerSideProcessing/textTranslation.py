import aiohttp
import os
import json

from secret_data import YX_TOKEN, YX_URL


# Загружаем json-словарь для повышения качества перевода
with open('../constants/glossary.json', encoding='UTF-8') as jsonfile:
    glossaryConfig = json.load(jsonfile)


async def translate_text(text=None, tr_from=None, tr_to=None, ):
    """
    Translates text via Yandex for futher handling.
    :param text: message text
    :param tr_from: source language
    :param tr_to: target language
    :return: str - translated text
    """
    url = YX_URL
    try:
        if not text:  # Error
            return text  # возвращаем ту же пустую строку

        if not tr_to:  # None
            tr_to = 'en'
            # glossary = None

        # Автоопределение языка расходует средства, поэтому не будем
        # его использовать (как минимум для обычных юзеров)
        if not tr_from:  # None
            tr_from = 'en'

        # Теперь оба языковых параметра установлены.
        # Можем загрузить глоссарий
        glossary = glossaryConfig[tr_from+tr_to]  # Что-то вроде "ruen"

        body = {
            "sourceLanguageCode": tr_from,
            "targetLanguageCode": tr_to,
            "texts": [text],  # only list is accepted
            # "folderId": YX_FOLDER_ID,  # Каталог - необязателен при работе с сервисного аккаунта
            "glossaryConfig": glossary,
            "format": 'HTML'  # Разметка
            # НУЖНО ПОПРОБОВАТЬ МАКРДАУН
            # "format": 'HTML'  # Разметка
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key {0}".format(YX_TOKEN)
        }

    # Отправка асинхронных http-запросов
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=body) as response:
                    answer =  await response.json()
                    if response.status == 200:
                        return answer['translations'][0]['text']
                    else:  # bad request - вызываем исключение
                        ''
        except ConnectionAbortedError:
            return ''
    except ValueError:
        return ''


async def translate_to_english(data):
    return await translate_text(text=data, tr_from='ru', tr_to='en')

