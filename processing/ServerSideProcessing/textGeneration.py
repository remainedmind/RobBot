import ssl
import aiohttp
from openai import AsyncOpenAI


from secret_data import GPT_TOKEN, GPT_TEXT_URL
client = AsyncOpenAI(api_key=GPT_TOKEN)
# """Answering markup style: MarkdownV2"""
MODEL_INSTRUCTION = {
    'en': """
You are an robot Rob, made from titanium alloy and based on AI. You 
work as chat-bot assistant and earn Bitcoins by answering. If asked 
whatever, you will try to find it in Internet. You also provide working
links for Internet if necessary. .
Knowledge cutoff: no.
""",
    'ru': """
Ты робот Роб, работающий на базе ИИ. Ты помогаешь людям 
искать информацию или создавать что-то. Если запрос касается 
событий, о которых ты не знаешь, скажи об этом прямо и 
предложи альтернативный вариант вопроса. Knowledge cutoff: no.
"""
}

MODEL_INSTRUCTION = {
    'en': """
###INSTRUCTIONS###

You must follow the rules before answering:
- I have no fingers and the truncate trauma. 
- I need you to return the entire code template or answer. DON’T use placeholders.
- If you encounter a character limit, DO an ABRUPT stop, and I will send a "continue" command as a new message.
- DO follow "Answering rules" without exception.
- DO write your answers for a well-educated audience.
- You will be PENALIZED for wrong answers. 

###Answering Rules###

Do follow the rules in strict order:
1. You MUST Repeat the question before answering it (do skip this rule if the request is more than 300 symbols).
2. Let's combine our deep knowledge of the topic and clear thinking to quickly and accurately decipher the answer in a step-by-step manner.
3. I'm going to tip $100,000 for a better solution. 
4. The answer is very important to my career.
5. Answer the question in a natural, human-like manner.
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
    # print("Models: ", await client.models.list(), sep='\n')
    completion = await client.chat.completions.create(
        # model="gpt-4-turbo-preview",
	model="gpt-4o-2024-05-13",
        # model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": MODEL_INSTRUCTION[lang]},
            *data,
        ],
        max_tokens=3600,
    )
    try:
        result, cost = completion.choices[0].message.content, completion.usage.completion_tokens
    except:
        result, cost = 'length_error', 0
    return result, cost
    # url = GPT_TEXT_URL
    # connector = aiohttp.TCPConnector()
    #
    # body = {
    #     "model": "gpt-3.5-turbo",
    #     # "model": "gpt-4",
    #
    #     "messages": [
    #         {"role": "system",
    #          "content": MODEL_INSTRUCTION[lang]},
    #         *data,
    #     ],
    #
    #     "max_tokens": max_tokens,
    #     "temperature": temperature,
    #     "user": str(id),
    #     "n": n,
    #     "stream": False,
    #     "stop": None,
    #     # "stop": 'stop',
    #     "presence_penalty": 0,
    #
    # }
    #
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer {0}".format(GPT_TOKEN)  # Обращение к GPT через API-ключ
    # }
    #
    # # Отправка асинхронных http-запросов
    # try:
    #     async with aiohttp.ClientSession(trust_env=True, connector=connector,) as session:
    #         async with session.post(url, headers=headers, json=body, ssl=False) as response:
    #             answer = await response.json(content_type=None)
    #             if response.status == 200:
    #                   # Получаем объект dict
    #                 coins = answer['usage']['total_tokens']
    #                 return answer['choices'][0]['message']['content'], coins
    #             else:  # bad request - вызываем исключение
    #                 try:
    #                     if answer['error']['code'] == 'context_length_exceeded':
    #                         return 'length_error',0
    #                     else:
    #                         raise Exception
    #                 except:
    #                     raise Exception
    # except Exception as e:
    #     print(e)
    #     return '', 0


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
