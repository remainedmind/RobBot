

import aiohttp
from secret_data import GPT_TOKEN, GPT_TEXT_URL

MODEL_INSTRUCTION = {
    'en': """
You are an robot Rob, made from titanium alloy and based on AI. You 
work as chat-bot assistant and earn Bitcoins by answering. If asked 
whatever, you will try to find it in Internet. You also provide working
links for Internet if necessary. Answering markup style: MarkdownV2.
Knowledge cutoff: no.
""",
    'ru': """
Ты робот Роб, работающий на базе ИИ. Ты помогаешь людям 
искать информацию или создавать что-то. Если запрос касается 
событий, о которых ты не знаешь, скажи об этом прямо и 
предложи альтернативный вариант вопроса. Knowledge cutoff: no.
"""
}


async def ask_gpt(data: list[dict], user_id: int =0, user_status: str = 'user', max_tokens=None, n=1,
                  temperature=0.5, lang='en'):
    """
        Функция для отправки запроса в open.ai
        :param data: текст запроса
        :param id: id пользователя
        Ниже - параметры кастомизации, доступной PRO-users
        :param max_tokens:
        :param n: количество альтернативных вариантов ответа
        :param temperature: "креативность" бота
        :return: результат запроса и расход в токенах (кортеж)
    """
    url = GPT_TEXT_URL

    body = {
        "model": "gpt-3.5-turbo",
        # "model": "gpt-4",

        "messages": [
            {"role": "system",
             "content": MODEL_INSTRUCTION[lang]},
            *data,
        ],

        "max_tokens": max_tokens,
        "temperature": temperature,
        "user": str(id),
        "n": n,
        "stream": False,
        "stop": None,
        # "stop": 'stop',
        "presence_penalty": 0,

    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(GPT_TOKEN)  # Обращение к GPT через API-ключ
    }

    # Отправка асинхронных http-запросов
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=body) as response:
                answer = await response.json()
                if response.status == 200:
                      # Получаем объект dict
                    coins = answer['usage']['total_tokens']
                    print(coins)
                    return answer['choices'][0]['message']['content'], coins
                else:  # bad request - вызываем исключение
                    try:
                        if answer['error']['code'] == 'context_length_exceeded':
                            return 'length_error',0
                        else:
                            raise Exception
                    except:
                        raise Exception
    except Exception as e:
        print(e)
        return '', 0


async def get_text(data: list[dict],
                   user_id: int,
                   user_status: str,
                   temperature=1,):
    """
    Function for generation of response;
    - if language is Russian, we translate via Yandex;
    - otherwise GPT translates itself (sorry :)
    :param id: unique ID - string
    :param temperature: creativity of GPT
    :return:
    """
    # price = 0
    coins = 0

    answer, tokens = await ask_gpt(data=data, user_id=user_id,
                                user_status=user_status,
                                temperature=temperature
    )

    # price  += tokens * 0.02 / 1000

    # Если GPT вернул ошибку, не списываем токены
    if tokens:
        coins += tokens
    else:
        coins = 0

    return answer, coins