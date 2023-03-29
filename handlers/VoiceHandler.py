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
from DELETEtextdata import properties, callback_answers, message_texts
from processing.LongAnswering import escort

from keyboards import ConversationContextKeyboard as concon
from const import VOICE_TRANSCRIBE_PRICE


import aiohttp
import asyncio

from pydub import AudioSegment


async def transcribe(file_id, lang=None) -> dict | None:
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
    duration = message.voice.duration  # in seconds
    try:
        file = await bot.get_file(file_id)
    except exceptions.TelegramBadRequest:  # Слишком большое сообщение
        return await message.reply('An error occurred while processing the voice. Please try again.')

    size = file.file_size/1000000

    if size >= 20:
        # Файлы больше 20 мб не принимаем
        await message.reply("Message is too long, we can't process it")

    file_path = file.file_path
    down_file = await bot.download_file(file_path)
    # Write the stuff

    with open(f"voices/{file_id}.ogg", "wb") as f:
        f.write(down_file.read())


    sound = AudioSegment.from_ogg(os.getcwd()+f"\\voices\\{file_id}.ogg")

    sound.export(f"voices/{file_id}.mp3", format="mp3")
    transcription, ans_message = await asyncio.gather(
        transcribe(file_id, lang),
        escort(message=message, lang=lang, target='voice')
    )

    # transcription = await transcribe(file_id, lang)
    answer = 'An error occurred while processing the voice. Please try again.'
    markup = None
    if transcription:
        text = transcription['text']
        if text:  # Not None
            # Запоминаем текст
            await state.update_data(voice_text = text)

            answer = message_texts['answering']['voice'][lang][3].format(text)
            markup = concon.voice_kb[lang]
        else:
            answer = "The message wasn't recognized: no one word was caught.\nTry again."
    answer = answer.replace('.', '\\.').replace('!', '\\!').replace('?', '\\?').replace('-', '\\-')
    try:
        await ans_message.edit_text(answer, parse_mode='MarkdownV2', reply_markup=markup)

        coins = duration / 60 * VOICE_TRANSCRIBE_PRICE
        print("Voice price:  ", coins)
    except exceptions.TelegramBadRequest:
        await ans_message.edit_text(answer, parse_mode=None, reply_markup=markup)
    try:
        os.remove(f"voices/{file_id}.ogg"), os.remove(f"voices/{file_id}.mp3")
    except FileNotFoundError:
        pass
