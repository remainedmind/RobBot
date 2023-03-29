"""

"""

from typing import Optional, Tuple
from aiogram import Bot, Router, F, exceptions

from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup
import asyncio

router = Router()  # [1]

from keyboards import ConversationContextKeyboard as conconkb

from processing.split_long_message import safe_split_text
from processing.ServerSideProcessing.textGeneration import get_text
from processing.ServerSideProcessing.photoGeneration import get_photo
from keyboards.ConversationContextKeyboard import Chat


from processing.ServerSideProcessing.voiceTranscription import transcribe



from const import VOICE_TRANSCRIBE_PRICE, MAX_DIALOGUE_SIZE

from aiogram.fsm.context import FSMContext

from middlewares.throttling import ThrottlingMiddleware

from processing.LongAnswerEscort import escort
from processing.SQL_processingg.SQL_high_level_processing import check_for_premium
from text_data.message_answers import answers_texts as ma_texts
from text_data.user_settings import PROPERTIES_DEFAULT_VALUES
from text_data.various import links_cover

router.message.middleware(ThrottlingMiddleware())
router.callback_query.middleware(ThrottlingMiddleware())

async def send_answer(answer_message: Message, answer: str, button: InlineKeyboardMarkup | None) -> Message | None:
    """
    Prepare text for Markdown parsing, split it in case it's long, and, finally, send it
    :param answer_message:
    :param answer:
    :param button:
    :return:
    """
    if len(answer) < 4000:
        try:
            mkdown_answer = answer
            # Подготовим текст для MarkdownV2
            [mkdown_answer := mkdown_answer.replace(c, "\\" + c) for c in '.!-+=|<>#']
            answer_msg = await answer_message.edit_text(
                mkdown_answer,
                parse_mode="MarkdownV2",
                reply_markup=button
            )

            # await mAA.answer("HELLO", entities=[Entity])
        except exceptions.TelegramBadRequest:
            answer_msg = await answer_message.edit_text(
                answer,
                parse_mode=None,
                reply_markup=button
            )
        return answer_msg
    else:  # Text is too long
        texts = await safe_split_text(answer)
        message = await answer_message.edit_text(texts[0])
        for text in texts[1:-1]:
            # Each message will be an answer for previous.
            message = await message.reply(text)
        await message.reply(text=texts[-1], reply_markup=button)


async def process_question(user_id: int, message: Message, user_info: dict, text: Optional[str] = None) -> Tuple[str, int, str]:
    """

    :param message: if we ask from typing, we extract the qustion text from here
    :param state: FSM
    :param text: if we ask after voice recognition, we provide this argument as a question
    :return:
    """
    lang = user_info['language']
    user_status = await check_for_premium(user_id)
    removed_old = False
    try:
        temperature = user_info['temperature']
    except KeyError:
        temperature = PROPERTIES_DEFAULT_VALUES['temperature']
    temperature /= 10

    try:
        dialogue: Chat = user_info['dialogue']
        is_chat = dialogue.active
    except KeyError:
        is_chat = False
        dialogue = None

    if not text:
        text = message.text
    if is_chat:
        tokens_limit = MAX_DIALOGUE_SIZE[user_status]
        await dialogue.add_user_message(text)
        # total_letters = sum([len(m['content']) for m in dialogue.chat])
        # print("TOTAL, ", total_letters)
        # if total_letters > MAX_DIALOGUE_LENGTH[user_status]:
        #     await dialogue.remove_old_messages()
        #     # We'll say to user that old messages was deleted
        #     removed_old = True


        response, ans_message = await asyncio.gather(
            get_text(data=dialogue.chat,
                     user_id=user_id,
                     user_status=user_status,
                     temperature=temperature),
            escort(user_status=user_status, message=message, lang=lang, target='text')
        )
        ans_text, coins = response[0], response[1]

        await dialogue.add_bot_message(ans_text)
        if coins > tokens_limit:
            # Delete it again
            await dialogue.remove_old_messages()
            removed_old = True
        elif ans_text == 'length_error':
            await dialogue.remove_old_messages()
            ans_text = ma_texts['answering']['error_dut_to_dialogue_limit'][lang]
            removed_old = False

        # await state.update_data(dialogue=dialogue)
        button = conconkb.reset_and_stop_kb[lang]

        # if coins > MAX_DIALOGUE_LENGTH[user_status]:
        #     await dialogue.remove_old_messages()
        #     # We'll say to user that old messages was deleted
        #     removed_old = True
    else:
        data = [{"role": "user", "content": text}]
        response, ans_message = await asyncio.gather(
            get_text(data=data,
                     user_id=user_id,
                     user_status=user_status,
                     temperature=temperature),
            escort(user_status=user_status, message=message, lang=lang, target='text')
        )
        ans_text, coins = response[0], response[1]
        button = conconkb.start_kb[lang]

    if not ans_text:
        ans_text = ma_texts['answering']['unknown_text_error'][lang]
        button = None
        coins = 0

    answer_msg = await send_answer(answer_message=ans_message, answer=ans_text, button=button)


    if answer_msg:
        # Check if there are any links in the message. If yes, we transform it to hypertext

        entities = answer_msg.entities
        # print(entities)
        if entities:
            text = answer_msg.text
            # entities.reverse()
            total_offset = 0
            for entity in entities:
                # If the answer contains ONLY uncovered link as entities, we
                # transform these to hyperlinks, which is better. Is there are any
                # code or may be hyperlinks itself, we don't do anything in order
                # to don't break down Markdown. Thus, if message is simple,
                # we can make it looks better, otherwise let's not make trouble
                # for ourselves

                if entity.type == 'url':
                    # Here we take into account that if we get code or e.t.c, then
                    # most probably URL isn't a first entity, so we don't need
                    # to check all entities before this loop

                    entity.type = 'text_link'
                    entity.offset -= total_offset
                    entity.url = text[entity.offset: entity.offset + entity.length]
                    if not 'http' in entity.url:
                        # Protect Telegram from mistakes
                        continue

                    hypertext = links_cover[lang]

                    text = text[:entity.offset] + hypertext + text[entity.offset + entity.length:]

                    entity.length = len(hypertext)

                    total_offset += len(entity.url) - entity.length

                    await asyncio.sleep(0.6)
                    try:
                        await answer_msg.edit_text(text, entities=entities, reply_markup=button)
                    except exceptions.TelegramBadRequest:
                        pass

                elif entity.type == 'text_link':

                    if len(entity.url) != entity.length:
                        # Then it's already a hyperlink, we don't need to change it
                        continue

                    entity.offset -= total_offset

                    if not 'http' in entity.url:
                        # Protect Telegram from mistakes
                        continue

                    hypertext = links_cover[lang]

                    text = text[:entity.offset] + hypertext + text[entity.offset + entity.length:]

                    entity.length = len(hypertext)

                    total_offset += len(entity.url) - entity.length

                    await asyncio.sleep(0.6)
                    try:
                        await answer_msg.edit_text(text, entities=entities, reply_markup=button)
                    except exceptions.TelegramBadRequest:
                        pass
                else:
                    # We just move offset to save the entity working
                    entity.offset -= total_offset

    return dialogue, coins, removed_old


async def process_voice(user_id: int, message: Message, state: FSMContext, bot: Bot) -> None:
    """

    :param message: if we ask from typing, we extract the qustion text from here
    :param state: FSM
    :param text: if we ask after voice recognition, we provide this argument as a question
    :return:
    """
    user_status = await check_for_premium(user_id)

    lang = (await state.get_data())['language']
    file_id = message.voice.file_id  # It will be name of file also

    try:
        file = await bot.get_file(file_id)
    except exceptions.TelegramBadRequest:  # Не получилось загрузить
        return await message.reply(ma_texts['answering']['unknown_voice_error'][lang])

    size = file.file_size / 1000000  # Get megabytes size

    if size >= 20:
        # Файлы больше 20 мб не принимаем
        return await message.reply(ma_texts['answering']['voice_is_too_long'][lang])

    file_path = file.file_path
    # file = await bot.download_file(file_path)

    response, ans_message = await asyncio.gather(
        transcribe(file_path, file_id, bot, lang),
        # transcribe(file, file_id, lang),
        escort(user_status=user_status, message=message, lang=lang, target='voice')
    )

    markup = None
    if response:
        text = response['text']
        if text:  # Not None
            # Запоминаем текст
            await state.update_data(voice_text=text)
            answer = ma_texts['answering']['voice'][lang][3].format(text)
            markup = conconkb.voice_kb[lang]
        else:  # not None but EMPTY
            answer = ma_texts['answering']['empty_voice'][lang]
    else:
        answer = ma_texts['answering']['unknown_voice_error'][lang]

    await send_answer(answer_message=ans_message, answer=answer, button=markup)

    duration = message.voice.duration  # in seconds
    coins = duration / 60 * VOICE_TRANSCRIBE_PRICE
    return coins




async def process_drawing(user_id, message: Message, text: str, user_info: dict) -> None:

    user_status = await check_for_premium(user_id)
    lang = user_info['language']
    try:
        photos_number = user_info['n_photos']
    except KeyError:
        # Настройки по умолчанию
        photos_number = PROPERTIES_DEFAULT_VALUES['n_photos']
    try:
        dim = user_info['dimension']
    except KeyError:
        dim = PROPERTIES_DEFAULT_VALUES['dimension']
    try:
        d_art = user_info['digital_art']
    except KeyError:
        d_art = PROPERTIES_DEFAULT_VALUES['digital_art']


    response, ans_message = await asyncio.gather(
        # ssp.get_text(dialogue.chat, message.from_user.id),
        get_photo(data=text, user_id=user_id, n=photos_number, dimension=dim, d_art=d_art, lang=lang),
        escort(user_status=user_status, message=message, lang=lang, target='photo')
    )
    photo_URLs, coins = response[0], response[1]
    if photo_URLs:
        await ans_message.edit_text(ma_texts['answering']['photo'][lang][-1])
    else:  # Failed
        # Сервер вернул пустой список
        await ans_message.edit_text(ma_texts['answering']['unknown_drawing_error'][lang])
        return 0

    photos_number = len(photo_URLs)  # Количество изображений

    if photos_number == 1:
        # Просто отправляем картинку
        await message.reply_photo(photo_URLs[0], allow_sending_without_reply=True)
    else:
        media = [  # Добавляем картинки в одну группу
            (InputMediaPhoto(media=url)) for url in photo_URLs
        ]
        await message.reply_media_group(media, allow_sending_without_reply=True)
    return coins



