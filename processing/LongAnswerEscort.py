import asyncio
import random
from aiogram import exceptions, Bot
from aiogram.types import Message
from aiogram.methods.send_chat_action import SendChatAction
# from aiogram.utils.chat_action import ChatActionSender
from processing.SQL_processingg.SQL_high_level_processing import check_for_premium
from text_data.message_answers import answers_texts as ma_texts
from const import DELAY

answer_delay = {
    'slow': ('🕐🕑🕒🕔🕕🕖🕘🕚🕛', "/-\\|/-\\|/"),
    'fast':  ('🕐🕒🕕🕘', "/-\\|")
}

async def get_midterm_emojis(speed):
    return random.choice(answer_delay[speed])


async def spin(msg, text, delay):
    """
    Функция для отображения загрузки
    :param msg: message to edit
    :param text: text to change (a bit)
    :param delay: ratio of speed
    :return:
    """
    text = text[:-3]+' '  # Удаляем многоточие
    # chars = "/-\\|" * delay
    speed = 'slow' if delay > 1 else 'fast'
    chars = await get_midterm_emojis(speed=speed)
    # chars = random.choice(('🕐🕑🕒🕔🕕🕖🕘🕚🕛', "/-\\|"*2))

    for c in chars:
        try:
            delay = 0.6
            await msg.edit_text(text + c)
        except exceptions.TelegramRetryAfter:
            # too high server load. Pass some actions
            delay = 2
        await asyncio.sleep(delay)





async def escort(user_status: str, message: Message, bot: Bot, target, lang='en', delay: int=2):
    """
    Предварительное редактирование сообщения. которео в итоге
    будет заменено на ответ Бота
    :param message:
    :param lang:
    :param target: что мы хотим получить: фото, текст, обработку голосового сообщения
    :param delay: задержка между промежуточными ответами.
    С помощью этого параметра можно плавно регулировать общую
    скорость ответа бота для обычных и премиум пользователей
    :return: None
    """
    # Мы редактируем сообщение на промежуточные сообщения из
    # списка: сначала первое, второе и т.д. В списке, связанном с
    # генерацией картинок, на один элемент больше. Поэтому нам
    # нужен сдвиг на 1:
    option = 1 * (target == 'photo')  #
    chat_id = message.chat.id
    delay = DELAY[user_status]
    # if user_status != 'user':
    #     delay = 1
    # ChatAction
    action = 'upload_photo' if target =='photo' else 'typing'

    answer = ma_texts['answering'][target][lang]
    reply = await message.reply(answer[0 + option])

    await bot(SendChatAction(chat_id=chat_id, action=action))
    # ЗАМЕНИТЬ НА: |
    #_________________
    # async with ChatActionSender.typing(chat_id=message.chat.id, bot=bot):
    #     await asyncio.sleep(10)
    # Do something long

    await asyncio.sleep(delay/2)

    await spin(reply, answer[1 + option], delay)
    # await asyncio.sleep(delay)
    # await SendChatAction(chat_id=id, action="typing")
    await reply.edit_text(answer[2 + option])
    # await asyncio.sleep(delay/2)
    return reply