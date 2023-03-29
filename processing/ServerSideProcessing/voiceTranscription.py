
import os
import aiohttp
from pydub import AudioSegment
from aiogram import Bot

from secret_data import GPT_TOKEN, GPT_WHISPER_URL

async def transcribe(file_path, file_id, bot: Bot, lang: str | None=None) -> dict | None:
    """
    Function for voice messages recognition;
    :param file_id: unique file id, which will be file name also
    :param lang: language will be mentioned to improve quality
    :return: if success, returns transcribed text
    """
    # Мы используем объект Бота здесь, а не в функции выше, чтобы
    # оптимизировать обработку сообщения (т.к. именно эту
    # функцию мы собираем в gather)
    file = await bot.download_file(file_path)

    url = GPT_WHISPER_URL

    # Write the stuff
    with open(os.getcwd()+f"/voices/{file_id}.ogg", "wb") as f:
        f.write(file.read())

    # Теперь нужно изменить формат
    sound = AudioSegment.from_ogg(os.getcwd()+f"/voices/{file_id}.ogg")

    sound.export(f"voices/{file_id}.mp3", format="mp3")



    headers = {
        "Authorization": "Bearer {0}".format(GPT_TOKEN),
        # "Content-Type": "multipart/form-data"
    }
    data = aiohttp.FormData()
    data.add_field("file",
                   # open("файлик.mp3", "rb"),
                   open(os.getcwd()+f"/voices/{file_id}.mp3", "rb"),
                   content_type="audio/mp3",
                   # filename="файлик.mp3"),
                    filename = f'{file_id}.mp3')
    data.add_field("model", "whisper-1")

    # if lang and lang != 'en':  # With english language set User can speak any language
    #     data.add_field("language", lang)

    # data.add_field("response_format", 'text')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                else:
                    result = None
    except:
        result = None
    finally:
        try:
            os.remove(os.getcwd()+f"/voices/{file_id}.ogg"), os.remove(f"voices/{file_id}.mp3")
        except FileNotFoundError:
            pass
        return result