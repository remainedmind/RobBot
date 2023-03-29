import ffmpeg
from aiogram import Router, F, Bot, exceptions
from aiogram.types import Message, CallbackQuery, BotCommand, Voice, Audio
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, Text, Filter, CommandObject
from aiogram.methods.send_message import SendMessage
from aiogram.utils.deep_linking import decode_payload, create_deep_link, create_start_link, create_telegram_link

from pathlib import Path

from const import PROMOCODE
from secret_data import TG_ADMIN_ID, GPT_TOKEN, GPT_WHISPER_URL
router = Router()  # [1]
from keyboards import BasicKeyboards as BK
from keyboards import DynamicKeyboards as DK
from processing import SQL_processingg as sqlp
from DELETEtextdata import properties, callback_answers


from keyboards import ConversationContextKeyboard as concon

# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
openai.api_key = GPT_TOKEN

import aiohttp

from pydub import AudioSegment

# load the ogg file


async def speech2text(file,
                  url='https://api.openai.com/v1/audio/transcriptions'):
    form = aiohttp.FormData()
    body = {
        "model": "whisper-1",
    }
    form.add_field('file', open('файлик.mp3', 'rb'), filename='файлик.mp3')
    form.add_field('model',  "whisper-1", content_type='multipart/form-data')
    # data = {'form': {'file': open('файлик.mp3', 'rb'),
    #         "model": "whisper-1",
    #         }
    # }
    data = {
        'file': open('файлик.mp3', 'rb'),
    }
    # with aiohttp.MultipartWriter('mixed') as mpwriter:
    headers = {
        "Content-Type": "multipart/form-data",
        "Authorization": "Bearer {0}".format(GPT_TOKEN)  # Обращение к GPT через API-ключ
    }

    # Отправка асинхронных http-запросов
    try:
        async with aiohttp.ClientSession() as session:
            # async with session.post(url, headers=headers, data=form, ) as response:
            async with session.post(url, headers=headers, data=data, ) as response:
                reader = aiohttp.MultipartReader.from_response(response)
                print(response)
                answer = await response.json()
                print(answer)
                if response.status == 200:
                      # Получаем объект dict
                    print(200, '\n\n', answer)
                else:  # bad request - вызываем исключение
                    raise Exception
    except Exception as e:
        raise
        return False

# import requests
#
# url = 'https://api.openai.com/v1/files/upload'
# files = {'file': open('file.mp3', 'rb')}
# headers = {
#     'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
#     'model': 'YOUR_MODEL_NAME'
# }
# response = requests.post(url, files=files, headers=headers)
# print(response.content)



async def transcribe(file_id, lang=None):
    """
    Function for voice messages recognition;
    :param file_id: unique file id, which will be file name also
    :param lang: language will be mentioned to improve quality
    :return: if success, returns transcribed text
    """

    url = GPT_WHISPER_URL
    headers = {
        "Authorization": "Bearer {0}".format(GPT_TOKEN),
        # "Content-Type": "multipart/form-data"
    }
    data = aiohttp.FormData()
    data.add_field("file",
                   # open("файлик.mp3", "rb"),
                   open(f"voices/{file_id}.mp3", "rb"),
                   content_type="audio/mp3",
                   # filename="файлик.mp3"),
                    filename = f'{file_id}.mp3')
    data.add_field("model", "whisper-1")

    if lang and lang != 'en':  # With english language set User can speak any language
        data.add_field("language", lang)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except:
        return None

import os



@router.message(F.voice)
async def command_start_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    """
    Function for handling voice messages for further recognition.
    """
    # Язык пригодится и для ответа, и для повышения качества расшифровки
    lang = (await state.get_data())['language']

    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    print(file.file_size)
    file_path = file.file_path
    down_file = await bot.download_file(file_path)
    # Write the stuff

    with open(f"voices/{file_id}.ogg", "wb") as f:
        f.write(down_file.read())



    # AudioSegment.converter = os.getcwd() + "\\ffmpeg.exe"
    # AudioSegment.ffprobe = os.getcwd() + "\\ffprobe.exe"



    # sound = AudioSegment.from_file(f"{os.getcwd()}/{file_id}.ogg", format="ogg")
    #
    # sound.export(f"{os.getcwd()}/{file_id}.mp3", format="mp3")


    sound = AudioSegment.from_ogg(os.getcwd()+f"\\voices\\{file_id}.ogg")

    sound.export(f"voices/{file_id}.mp3", format="mp3")

    # with open(f"{file_id}.mp3", "rb") as f:
    #     transcript = openai.Audio.transcribe("whisper-1", f)
    #     print(transcript['text'])
    # fifa = open(f"{file_id}.mp3", 'rb')
    # fifa = open(f"файлик.mp3", 'rb')
    # print(fifa.name)
    # # print(down_file)
    # # print(down_file.close())
    # # fff = down_file.read()
    # # print(fff)
    # # audio_file= open(file_path, "rb")
    # transcript = openai.Audio.transcribe("whisper-1", fifa)
    # transcript = openai.Audio.transcribe("whisper-1", down_file.read())
    # text = transcript['text']

    transcription = await transcribe(file_id, lang)
    answer = 'An error occurred while processing the voice. Please try again.'
    markup = None
    if transcription:
        text = transcription['text']
        if text:  # Not None
            # Запоминаем текст
            await state.update_data(voice_text = text)

            answer = "*That's what I heard:*\n\n `{}`\n\n *Would you like to ask that?*".format(text)
            markup = concon.voice_kb[lang]
        else:
            answer = "The message wasn't recognized: no one word was caught.\nTry again."
    answer = answer.replace('.', '\\.').replace('!', '\\!').replace('?', '\\?').replace('-', '\\-')
    try:
        await message.reply(answer, parse_mode='MarkdownV2', reply_markup=markup)
    except exceptions.TelegramBadRequest:
        await message.reply(answer, parse_mode=None, reply_markup=markup)
    try:
        os.remove(f"voices/{file_id}.mp3"), os.remove(f"voices/{file_id}.ogg")
    except FileNotFoundError:
        pass
