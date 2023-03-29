from aiogram import F
from aiogram.filters import Command, Text, Filter, or_f
from aiogram import Router
from aiogram.types import Message
from app.finite_state_machine import UserStates
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Text, Filter
from text_data.message_answers import answers_texts as ma_texts
from const import PROMOCODE
router = Router()  # [1]


@router.message(UserStates.need_to_unblock_bot)
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
    await message.answer(ma_texts['start']['failed'][lang])


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

@router.message(F.photo)
async def photo_msg(message: Message, state: FSMContext):
    print(await state.get_state())
    await message.answer("Это точно какое-то изображение!")
