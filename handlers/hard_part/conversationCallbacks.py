"""

"""

from aiogram import Bot, Router, F, exceptions

from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command, Text, Filter, or_f, invert_f

  # [1]


from keyboards import ConversationContextKeyboard as conconkb

from aiogram.fsm.context import FSMContext

# from aiogram.dispatcher.filters.state import State, StatesGroup


from middlewares.BalanceCheck import BalanceCheckMiddleware
from text_data.message_answers import answers_texts as ma_texts
from text_data import callback_answers


from processing.SQL_processingg import SQL_high_level_processing as sql_high_p
from handlers.hard_part.conversationHelpers import process_question, send_answer
from payments.pay_keyboards import buy_sub_kb
from app.finite_state_machine import UserStates


router = Router()
router.callback_query.middleware(BalanceCheckMiddleware())
router.callback_query.filter(invert_f(UserStates.need_to_unblock_bot))

@router.callback_query(conconkb.ConversationCallback.filter(F.data == 'dialogue'))
async def callbacks_num_change_fab(
        callback: CallbackQuery,
        callback_data: conconkb.ConversationCallback,
        state: FSMContext
):
    lang = (await state.get_data())['language']

    try:
        dialogue = (await state.get_data())['dialogue']
    except KeyError:
        dialogue = conconkb.Chat()
    action = callback_data.action
    if action == 'start':
        question = callback.message.reply_to_message.text
        answer = callback.message.text
        await dialogue.start_chat()
        await dialogue.add_user_message(question)
        await dialogue.add_bot_message(answer)
    elif action == 'reset':
        await dialogue.reset_chat()
    elif action == 'stop':
        await dialogue.stop_chat()

    await state.update_data(dialogue=dialogue)
    await callback.message.edit_reply_markup()
    await callback.answer(callback_answers.conversation[action][lang])
    await callback.message.reply(ma_texts['conversation'][action][lang])


@router.callback_query(conconkb.ConversationCallback.filter(F.data == 'voice'),  flags={'coins_minimum': 0})
async def callbacks_num_change_fab(
        callback: CallbackQuery,
        callback_data: conconkb.ConversationCallback,
        state: FSMContext
):
    user_id = callback.from_user.id
    user_info = await state.get_data()
    # info = (await state.get_data())
    lang = user_info['language']
    action = callback_data.action
    await callback.message.edit_reply_markup()
    if action == 'pass':
        await callback.answer(callback_answers.forget_action[lang])
    elif action == 'ask':
        try:
            question = user_info['voice_text']
            user_info = await state.get_data()
            dialogue, coins, removed_old = await process_question(user_id=user_id, message=callback.message, user_info=user_info, text=question)
            if dialogue:
                await state.update_data(dialogue=dialogue)
            await sql_high_p.change_coins_balance(user_id, coins)
            await state.update_data(voice_text=None)  # Clear
            if removed_old:
                await callback.message.answer(ma_texts['answering']['dialogue_limit'][lang], reply_markup=buy_sub_kb[
                                     await sql_high_p.check_for_premium(user_id)
                                 ][lang])
        except KeyError:
            await callback.message.reply(ma_texts['answering']['error_with_voice_answering'])

