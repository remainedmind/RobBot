"""

"""
import json, pickle
from aiogram import Bot, Router, F, exceptions
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.utils.chat_action import ChatActionSender

from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command, Filter, or_f, invert_f

from keyboards import BasicKeyboards as bkb

import re

from aiogram.fsm.context import FSMContext

# from aiogram.dispatcher.filters.state import State, StatesGroup


from middlewares.throttling import ThrottlingMiddleware
from middlewares.BalanceCheck import BalanceCheckMiddleware
from text_data.message_answers import answers_texts as ma_texts
from text_data.various import string_for_re_searching, words_to_image
from handlers.hard_part.conversationHelpers import process_question, send_answer, process_voice, process_drawing

from app.finite_state_machine import UserStates
from processing.SQL_processingg import SQL_high_level_processing as sql_high_p
from payments.pay_keyboards import buy_sub_kb


router = Router()
router.message.middleware(BalanceCheckMiddleware())
router.callback_query.middleware(BalanceCheckMiddleware())

router.message.middleware(ThrottlingMiddleware())
router.callback_query.middleware(ThrottlingMiddleware())
router.message.filter(invert_f(UserStates.need_to_unblock_bot))




@router.message(Command(commands=["ask"]), flags={"throttling": 10, 'coins_minimum': 0})
async def command_start_handler(message: Message, state: FSMContext, command: Command, bot: Bot) -> None:
    user_id = message.from_user.id
    param = command.args
    user_info = await state.get_data()
    lang = user_info['language']
    await state.set_state(UserStates.main)
    if param:
        # response = (await asyncio.gather(process_question(message=message, state=state, text=param), escort(message=message, lang=lang, target='text')))
        dialogue, coins, removed_old = await process_question(user_id=user_id, message=message, bot=bot, user_info=user_info, text=param)
        if dialogue:
            dialogue = pickle.dumps(dialogue).hex()
            # dialogue = pickle.loads(bytes.fromhex(dialogue))
            await state.update_data(dialogue=dialogue)
        if removed_old:
            await message.answer(ma_texts['answering']['dialogue_limit'][lang],
                                 reply_markup=buy_sub_kb[
                                     await sql_high_p.check_for_premium(user_id)
                                 ][lang])
        await sql_high_p.change_coins_balance(user_id, coins)
    else:
        lang = user_info['language']
        await message.reply(ma_texts['answering']['empty command'][lang])

@router.message(Command(commands=["image"]), flags={"throttling": 10, 'coins_minimum': 600})
async def draw(message: Message, command: Command, state: FSMContext, bot: Bot) -> None:
    param = command.args
    user_id = message.from_user.id
    user_info = await state.get_data()
    if param:
        coins = await process_drawing(user_id, message, bot, param, user_info)
        await sql_high_p.change_coins_balance(user_id, coins)
        await state.set_state(UserStates.main)
    else:
        lang = user_info['language']
        await state.set_state(UserStates.image_generation)
        await message.reply(ma_texts['answering']['photo'][lang][0], reply_markup=bkb.cancel_kb[lang])

@router.message(F.text.startswith(words_to_image), F.text.as_("text"),  flags={"throttling": 10, 'coins_minimum': 600})
async def draw(message: Message, text, state: FSMContext, bot: Bot) -> None:
    user_id = message.from_user.id
    user_info = await state.get_data()
    match = re.search(string_for_re_searching, string=text.lower())
    # We don't need to check match because we already handled proper message
    text = text[match.end():]
    await state.set_state(UserStates.main)
    coins = await process_drawing(user_id, message, bot, text, user_info)
    await sql_high_p.change_coins_balance(user_id, coins)


@router.message(UserStates.image_generation, F.text,  flags={"throttling": 10, 'coins_minimum': 600})
async def command_start_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    """

    :param message:
    :param state:
    :return:
    """
    user_id = message.from_user.id
    user_info = await state.get_data()
    await state.set_state(UserStates.main)
    coins = await process_drawing(user_id, message, bot, message.text, user_info)
    await sql_high_p.change_coins_balance(user_id, coins)


# @router.message(UserStates.main, F.text,  flags={"throttling": 20})
@router.message(F.text,  flags={"throttling": 10, 'coins_minimum': 0})
async def command_start_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    """

    :param message:
    :param state:
    :return:
    """
    user_id = message.from_user.id
    user_info = await state.get_data()
    lang = user_info['language']
    await state.set_state(UserStates.main)

    dialogue, coins, removed_old = await process_question(user_id, message, bot, user_info)
    if dialogue:
        dialogue = pickle.dumps(dialogue).hex()
        await state.update_data(dialogue=dialogue)
    if removed_old:
        status = await sql_high_p.check_for_premium(user_id)
        markup = buy_sub_kb[status]
        if markup:
            markup = markup[lang]

        await message.answer(ma_texts['answering']['dialogue_limit'][lang], reply_markup=markup, parse_mode="MarkdownV2")
    await sql_high_p.change_coins_balance(user_id, coins)


@router.message(F.voice,  flags={"throttling": 10, 'coins_minimum': 0})
async def voice_message_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    """
    Function for handling voice messages for further recognition.

    """
    user_id = message.from_user.id
    await state.set_state(UserStates.main)

    coins = await process_voice(user_id, message, state, bot)
    await sql_high_p.change_coins_balance(user_id, coins)
