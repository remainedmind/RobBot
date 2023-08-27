"""

"""
import pickle
from datetime import datetime

import aiogram.exceptions
from aiogram import Router, F, md, html, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, WebAppData, web_app_info, sent_web_app_message
from aiogram.filters import CommandStart, Command, Filter, CommandObject, invert_f, or_f, and_f
from aiogram.utils.deep_linking import decode_payload
from aiogram.methods.send_message import SendMessage

# from secret_data import TG_ADMIN_ID
from text_data.user_settings import PROPERTIES_DEFAULT_VALUES


from keyboards import BasicKeyboards as bkb

from processing.SQL_processingg import SQL_high_level_processing as sql_high_p
from text_data.message_answers import answers_texts as ma_texts


from app.finite_state_machine import UserStates

from filters.PromoCode import IsPromocode

from keyboards.CommunicationWithAdmin import confirm_feedback_kb
from processing.AccountProcessing import get_account_details
from processing.LightFucntions import get_emoji

from app.set_menu_commands import set_personal_menu_commands
from keyboards import ConversationContextKeyboard as conconkb

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject, state: FSMContext, bot: Bot) -> None:
    """

    """
    user_id, chat_id, name, username = (
        message.from_user.id, message.chat.id, message.from_user.first_name,
        message.from_user.username
    )
    await state.set_state(UserStates.need_to_unblock_bot)

    lang = message.from_user.language_code
    if not lang in ('en', 'ru'):
        lang = 'en'

    await message.answer(ma_texts['start']['hello'][lang].format(
        name
    ),
        # reply_markup=bkb.language_kb
    reply_markup = bkb.start_kb[lang]
    )
    now = message.date.utcnow()  # UTC TIME
    # if user_id == chat_id:
    new_user = await sql_high_p.add_new_user(user_id, username, lang, now)

    # If it's new user, we check for referrer
    if new_user:
        await state.update_data(**PROPERTIES_DEFAULT_VALUES)

        args = command.args
        if args:
            try:
                # Получаем id
                ref_id = decode_payload(args)
                ref_id = int(ref_id)
                reward = await sql_high_p.add_referral(ref_id, user_id)
                if reward:
                    referrer_lang = await sql_high_p.get_lang(ref_id)
                    await bot(SendMessage(chat_id=ref_id, text=ma_texts['referral']['new_referral'][referrer_lang].format(reward)))
            except (UnicodeDecodeError, ValueError):
                pass
    await state.update_data(language=lang)



@router.message(Command(commands=["main"]))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """

    """
    lang = (await state.get_data())['language']
    await state.set_state(UserStates.main)
    await message.answer(ma_texts['main'][lang], reply_markup=bkb.main_page_kb[lang])


@router.message(Command(commands=["test"]))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """

    """
    lang = (await state.get_data())['language']
    await state.set_state(UserStates.main)
    await message.answer(ma_texts['main'][lang], reply_markup=bkb.test_kb)



from aiogram.utils.web_app import safe_parse_webapp_init_data
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

async def check_data_handler(request: Request):
    print('получили реквест')
    bot: Bot = request.app["bot"]

    data = await request.post()  # application/x-www-form-urlencoded
    try:
        data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    except ValueError:
        return json_response({"ok": False, "err": "Unauthorized"}, status=401)
    print(json_response({"ok": True, "data": data.user.model_dump_json()}))


@router.message(WebAppData)
async def command_start_handler(state: FSMContext, web: WebAppData) -> None:
    """

    """
    print(web)
    # await message.answer("GOT", reply_markup=bkb.test_kb)

@router.message()
async def command_start_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    It's an old command. When recieved, user's menu will be changed to new format
    """
    lang = (await state.get_data())['language']
    user_id, chat_id = message.from_user.id, message.chat.id

    await set_personal_menu_commands(
        chat_id=chat_id, user_id=user_id, lang=lang, bot=bot
    )
    await message.answer(ma_texts['switch'][lang])


@router.message(Command(commands=["help"]))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """

    """
    await state.set_state(UserStates.main)
    lang = (await state.get_data())['language']
    # await message.answer(ma_texts['help'][lang], reply_markup=bkb.cancel_kb[lang])
    await message.answer(ma_texts['help'][lang], reply_markup=bkb.help_kb[lang])


# from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup,
#                            KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
# from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData
# from aiogram.types.web_app_info import WebAppInfo


@router.message(Command(commands=["dice"]))
async def dice_command(message: Message) -> None:
    """
       Simple dice. Artificial - yes :)   Intelligence - no :(
       """

    emoji = await get_emoji(message.message_id)
    await message.answer_dice(emoji=emoji)



@router.message(Command(commands=["account"]))
async def account_command_handler(message: Message, state: FSMContext) -> None:
    """
    Command to see information about yourself
    """
    await state.set_state(UserStates.main)



    lang = (await state.get_data())['language']
    await message.answer(text=await get_account_details(
        message.from_user.id, lang
    ), reply_markup=bkb.account_from_command_kb[lang])



@router.message(Command(commands=["reset"]))
async def callbacks_num_change_fab(
        message: Message, state: FSMContext
):
    lang = (await state.get_data())['language']

    try:
        dialogue = (await state.get_data())['dialogue']
        dialogue: conconkb.Chat = pickle.loads(bytes.fromhex(dialogue))
    except KeyError:
        dialogue = conconkb.Chat()

    await dialogue.reset_chat()

    # Transform Object instance to string to make it storable
    dialogue = pickle.dumps(dialogue).hex()
    await state.update_data(dialogue=dialogue)

    # await callback.message.edit_reply_markup()
    # await callback.answer(callback_answers.conversation[action][lang])
    await message.reply(ma_texts['conversation']['reset'][lang])


@router.message(or_f(F.photo, F.text, F.document),
                or_f(
                    F.text.startswith('Admin'),  F.text.startswith('Админ'), F.caption.startswith("Admin")
                )
                )
async def send_message2admin(message: Message, state: FSMContext, bot: Bot) -> None:
    lang = (await state.get_data())['language']

    if message.photo:  # We got photo
        text = message.caption[7:]
        sender = message.answer_photo(photo=message.photo[0].file_id, caption=text, reply_markup=confirm_feedback_kb[lang], parse_mode=None)
    elif message.document:  # We got docs
        text = message.caption[7:]
        sender = message.answer_document(document=message.document.file_id, caption=text,
                                      reply_markup=confirm_feedback_kb[lang], parse_mode=None)
    else:  # text only
        text = message.text[7:]
        sender = message.answer(text=text, reply_markup=confirm_feedback_kb[lang], parse_mode=None)
    if text:
        await message.reply(ma_texts['feedback']['show_message'][lang])
        feedback = await sender
    else:
        await message.reply(ma_texts['feedback']['empty'][lang])


@router.message(F.text.startswith('!'), IsPromocode())
async def check_promocode(message: Message, state: FSMContext, validity: bool, bonus: int) -> None:
    """
    Promo code handling.
    All promo codes start with "!", thus we can easily pass
    further promo code checking with our filter:
    Firstly we quickly check whether it starts with ! of not, so we call our
    heavy filter only in case it's supposed to be a promo
    """
    lang = (await state.get_data())['language']
    id = message.from_user.id

    if validity and bonus:  # Then we give bonus
        await sql_high_p.change_coins_balance(
            id=id, charge=bonus, method='put'
        )
    await message.reply(ma_texts['promocode'][validity][lang])


