"""
Модуль с хэндлерами для команд, предназначенных только
для админа
"""
from aiogram import Router, F, md, exceptions
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.methods.send_message import SendMessage

from keyboards import BasicKeyboards as bkb
router = Router()  # [1]
from filters.AdminFilter import IsAdmin

from app.finite_state_machine import UserStates
from text_data.message_answers import answers_texts as ma_texts, admin_command_answers
from keyboards.CommunicationWithAdmin import confirm_answer_kb
from keyboards.AdminKeyboard import AdminCallbacks, build_keyboard
from processing.SQL_processingg import SQL_high_level_processing as sql_high_p
from processing import timeProcessing as timep



from text_data.various import expiry_format
from text_data import callback_answers
from const import DATABASE

# Добавим фильтр
router.message.filter(IsAdmin())

# Ниже - команды админа
@router.message(Command(commands=["myusers"]))  # [2]
async def cmd_start(message: Message):
    users = await sql_high_p.get_customers_data(method='amount')
    if users:
        await message.reply(admin_command_answers['amout_of_users'].format(users[0][0]))
    try:
        database = FSInputFile(DATABASE)
        await message.answer_document(document=database, caption="DATABASE:")
    except Exception as e:
        await message.reply(f'!! ERROR: {e}')


@router.message(Command(commands=["spam"]))  # [2]
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(UserStates.spamming)
    await message.answer(admin_command_answers['spam_first'], reply_markup=bkb.cancel_kb['en'])


@router.message(Command(commands=["manage"]))  # [2]
async def cmd_start(message: Message, command: Command):
    user = command.args  # id or nickname
    if not user:
        answer = 'Empty command\.'
        markup = None
    else:
        info = await sql_high_p.get_user_info_quickly(user)
        if not info:  # Try with nickname
            info = await sql_high_p.get_info_by_nickname(user[1:])

        try:
            # Collect all data about user
            info['balance'] = md.quote(str(info['balance']))  # in case it's negative
            if info['prem_expires']:
                expiry = await timep.get_expiry_date(info['prem_expires'])
                info['prem_expires'] = md.quote(expiry.strftime(expiry_format['status_until']['en']))
            answer = admin_command_answers[
                'info_about_user'
            ].format(**info)
            markup = await build_keyboard(info['id'], action='manage', status=info['status'])
        except TypeError:  # empty data
            answer = '\!\! User not found\.'
            markup = None

    await message.answer(answer,
                         # parse_mode='MarkDownV2',
                         reply_markup=markup)


@router.callback_query(AdminCallbacks.filter())
async def confirm_feedback(
        callback: CallbackQuery,
        callback_data: AdminCallbacks,
        state: FSMContext,
):
    user_id = callback_data.user_id
    action = callback_data.action
    status = callback_data.status
    data = callback_data.data
    if action == 'change':
        if data == "balance":
            await state.update_data(user2give_coins =user_id)
            await callback.message.reply('How much coins you want to give?', reply_markup=bkb.cancel_kb['en'])
            await state.set_state(UserStates.coins_giving)
        elif data == "status":
            await callback.message.reply('Confirm setting the status:', reply_markup=await build_keyboard(user_id, action='change', status=status, data='status'))
    elif action == 'confirm':
        await state.set_state(UserStates.main)
        if data == "status":
            now = callback.message.date.utcnow()  # UTC TIME
            # By default, we give premium for 30 days
            success = await sql_high_p.set_new_status(user_id, status, now, period={'days': 30})
            if success:
                await SendMessage(chat_id=user_id, text=ma_texts['new_status'][status]['en'])
                await callback.message.reply(admin_command_answers['new_status'].format(status))
    elif action == 'send_spam':
        await callback.message.reply(admin_command_answers['spam_third'],
                                     reply_markup=await build_keyboard(user_id, action=action)
        )
    elif action == 'confirm_spam':
        # Sending the messages
        dataset = await sql_high_p.get_customers_data()
        black_list = await callback.message.reply('BLACK LIST:')
        for client in dataset:
            user_to_sent = client[0]  # ID
            user_lang = client[6]  # language
            if user_lang == data or data == 'all':  # Audience
                try:
                    await SendMessage(chat_id=user_to_sent, text=callback.message.html_text, parse_mode='HTML')
                except exceptions.TelegramForbiddenError:
                    await black_list.edit_text(
                        black_list.text + f"\n<code>{user_to_sent}</code>;"
                    )
                except exceptions.TelegramBadRequest:
                    raise
        await callback.message.edit_text(admin_command_answers['spam_final']
        )
        await state.set_state(UserStates.main)

    elif action == 'cancel':
        await callback.answer(callback_answers.forget_action['en'])
        await callback.message.delete_reply_markup()
        await state.set_state(UserStates.main)

@router.message(Command(commands=["answer"]))
async def message_to_user(message: Message, command: Command, state: FSMContext):
    """
    Command for Admin to contact with customers
    """

    # id = message.from_user.id
    user = command.args
    if not command.args:  # Отправлена команда без текста
        return await message.reply("Empty command.")

    await message.reply("OK, now send the text to forward", reply_markup=bkb.cancel_kb['en'])
        # Запоминаем данные для дальнейшей пересылки
    await state.set_state(UserStates.answer2user)
    await state.update_data(user2contact=user)


@router.message(F.text, UserStates.spamming)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """

    :param message:
    :param state:
    :return:
    """
    text = message.text
    await message.reply(admin_command_answers['spam_second'])
    await message.answer(text=text, reply_markup=await build_keyboard(action='send_spam'), parse_mode=None)


@router.message(F.text, UserStates.answer2user)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """

    :param message:
    :param state:
    :return:
    """
    text = message.text
    await message.reply(ma_texts['feedback']['message_for_user'])
    await message.answer(text=text, reply_markup=confirm_answer_kb, parse_mode='HTML')


@router.message(F.text, UserStates.coins_giving)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """

    :param message:
    :param state:
    :return:
    """
    text = message.text
    user_id = (await state.get_data())['user2give_coins']
    try:
        try:
            charge = int(message.text)
        except ValueError:
            return await message.reply('We need a number!')
        success = await sql_high_p.change_coins_balance(user_id, charge, method='put')
        if success:
            if charge > 0:
                # We notice the user
                await SendMessage(chat_id=user_id, text=ma_texts['got_coins']['en'].format(charge))
            await message.reply(admin_command_answers['new_balance'].format(charge))
        else:
            await message.reply('Operation failed!')
        await state.set_state(UserStates.main)
    except Exception as e:
        await message.reply(f'!! UNKNOWN ERROR: {e}')
