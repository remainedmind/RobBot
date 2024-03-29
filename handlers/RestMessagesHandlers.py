from aiogram import F
from aiogram.filters import Command, Filter, or_f
from aiogram import Router
from aiogram.types import Message
from app.finite_state_machine import UserStates
from aiogram.fsm.context import FSMContext
from text_data.message_answers import answers_texts as ma_texts
router = Router()  # [1]


@router.message(F.data, UserStates.need_to_unblock_bot)
async def command_start_handler(message: Message) -> None:
    """

    :param message:
    :param state:
    :return:
    """
    # id = message.from_user.id
    print(message)
    lang = message.from_user.language_code
    if not lang in ('en', 'ru'):
        lang = 'en'
    pass




@router.message(UserStates.need_to_unblock_bot)
async def answer_2_unregistered_user(message: Message) -> None:

    user_id = message.from_user.id
    chat_id = message.chat.id
    lang = message.from_user.language_code
    if not lang in ('en', 'ru'):
        lang = 'en'
    if chat_id == user_id:
        ans = ma_texts['start']['restart'][lang]
    else:
        ans = ma_texts['start']['failed'][lang]

    await message.answer(ans)

@router.message(or_f(F.text, F.voice))
async def command_start_handler(message: Message) -> None:
    """

    :param message:
    :param state:
    :return:
    """
    # id = message.from_user.id
    lang = message.from_user.language_code
    if not lang in ('en', 'ru'):
        lang = 'en'
    await message.answer(ma_texts['start']['restart'][lang])

@router.message(or_f(F.photo, F.document))
async def photo_msg(message: Message, state: FSMContext):
    lang = message.from_user.language_code
    if not lang in ('en', 'ru'):
        lang = 'en'
    await message.answer(ma_texts["unexpected_image"][lang])
