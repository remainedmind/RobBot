import aiohttp
from secret_data import GPT_TOKEN, GPT_IMAGE_URL
from constants.const import PHOTO_GENERATION_PRICE
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key=GPT_TOKEN)


async def get_photo(
        data, user_id: int=None, dimension=256, n=1,
        d_art=True, lang=None, url=GPT_IMAGE_URL):
    """
      Функция для отправки запроса в open.ai
      :param data: текст запроса
      :param id: id пользователя в формате строки
      Ниже - параметры кастомизации, доступной PRO-users
      :param dimension: разрешение изображения
      :param n: количество изображений
      :param d_art: если True, автоматически дописываем digital art в конец запроса
      :param lang: language
      :return: url картинки и расход в токенах (кортеж)
    """
    if not data:  # In case it's '', which is error
        return data

    coins = PHOTO_GENERATION_PRICE[dimension] * n

    # if lang == 'ru':  # translate 2 English
    #     # Прибавляем количество токенов, затраченное для перевода
    #     coins += len(data)
    #     # price  += len(data)/1000* 4.92/USDtoRUB  # В долларах
    #     data = await translate_text(text=data, tr_from=lang)

    if d_art:
        data += '. Digital art.'

    # body = {
    #     "prompt": data,
    #     "size": f"{dimension}x{dimension}",
    #     "n": n,
    #     "user": str(user_id)  # API просит строки
    # }
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer {0}".format(GPT_TOKEN)}
    response = await client.images.generate(
        model="dall-e-3",
        prompt=data,
        # size=f"{dimension}x{dimension}",
        size="1024x1024",
        quality="standard",
        n=1,  # Only n=1 can be used.
        user=str(user_id)
    )
    image_urls = tuple([d.url for d in response.data])
    return image_urls, coins
    # print(response.data[0].url)
    # image_url = response.data[0].url

    #         {"role": "system",
    #          "content": MODEL_INSTRUCTION[lang]},
    #         *data,
    #     ])
    # try:
    #     result, cost = completion.choices[0].message.content, completion.usage.completion_tokens
    # except:
    #     result, cost = 'length_error', 0
    # return result, cost

    # Отправка асинхронных http-запросов
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=headers, json=body) as response:
    #         if response.status == 200:  # Success
    #             answer = await response.json()  # Получаем объект dict
    #             try:
    #                 # Возвращаем все изображения и затраченные монеты
    #                 return tuple(i['url'] for i in answer["data"]), coins
    #                 # return answer["data"][0]["url"]
    #             except Exception as e:
    #                 return '', 0
    #         else:  # bad request
    #             return '', 0