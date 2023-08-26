import datetime
import os

import aiosqlite
from aiogram import Bot, exceptions
from processing.SQL_processingg import SQL_high_level_processing as sql_high_p
from processing.timeProcessing import calculate_renew_time, get_expiry_date
from text_data.message_answers import answers_texts as ma_texts
from keyboards.BasicKeyboards import subscribe_to_ru_channel_kb
from constants.const import DATABASE, DEFAULT_BALANCE, REFERRAL_RATIO
from secret_data import TG_RU_CHANNEL_ID, TG_SUPPORT_ID

SLEEP_TIME = 15

# async def behind_loop(bot: Bot):
#     """
#     Constant updating of coins and user status
#     """
#     # black_list = await bot.send_message(
#     #     chat_id=TG_SUPPORT_ID,
#     #     text='BLACK LIST:'
#     # )
#     # bad_users = set()
#     # Here we create individual connection
#     async with aiosqlite.connect(DATABASE) as con:
#
#         while True:
#             await asyncio.sleep(SLEEP_TIME)
#             now = datetime.datetime.utcnow()
#
#             dataset = await sql_high_p.get_customers_data(method='data', con=con)
#             if not dataset:
#                 # Dataset is empty yet
#                 continue
#
#             for client in dataset:
#                 # Формат: (id, 'name'', 'status', date like '199912312359', balance, referrals, 'language)
#                 client_id = client[0]
#                 name = client[1]
#                 status = client[2]
#                 expiry = client[3]
#                 balance = client[4]
#                 referrals = client[5]
#                 lang = client[6]
#                 prem_expires = client[9]
#
#                 # Проверим, подписан ли пользователь на канал
#                 try:
#                     user_channel_status = (
#                         await bot.get_chat_member(chat_id=TG_RU_CHANNEL_ID, user_id=client_id)
#                     ).status
#
#                     sub = (user_channel_status not in ('left', 'kicked'))  # True, если подписан
#
#                 except exceptions.TelegramBadRequest as e:
#                     # Пользователь не найден
#                     # Или самого бота нет в канале
#                     sub = False
#                 except Exception as e:
#                     # raise
#                     sub = False
#                     await bot.send_message(TG_SUPPORT_ID, "An error occurred while updating the coins:".upper() + e)
#                 # continue
#
#
#                 sec_before_update = await calculate_renew_time(
#                     now=now,
#                     future=expiry
#                 )
#
#                 if sec_before_update < SLEEP_TIME:  # Время до обновления меньше заданного (или отрицательное)
#
#                     default_balance = DEFAULT_BALANCE[status]['general']
#
#                     # Добавим проценты к монетам за каждого реферала
#                     ref_reward = round(
#                         REFERRAL_RATIO * referrals * default_balance
#                     )
#                     default_balance += ref_reward
#
#                     # Добавим монет за подписку на канал
#                     if sub:
#                         sub_reward = DEFAULT_BALANCE[status]['sub']
#                     else:
#                         sub_reward = 0
#
#                     default_balance += sub_reward
#
#                     # Теперь, если пользователь потратил хоть немного токенов - обновим их
#                     new_balance = max(balance, default_balance)
#
#                     update_notice = default_balance > balance
#
#                     await sql_high_p.change_coins_balance(
#                         id=client_id, charge=new_balance, method='update', date=now, con=con
#                     )
#                     if update_notice:
#                         markup = None
#                         answer_text = ma_texts['auto_update'][lang].format(ref_reward)
#                         if lang == 'ru':
#                             answer_text += ma_texts['auto_update']['ru_channel_sub'].format(sub_reward)
#                             if not sub:
#                                 markup = subscribe_to_ru_channel_kb
#                         try:
#                             # Если баланс изменился - отправляем уведомление
#
#                             await bot.send_message(
#                                 chat_id=client_id, text=answer_text, reply_markup=markup)
#                         except exceptions.TelegramForbiddenError:  # Бот в чс
#                             pass
#                             # bad_users.add((client_id, name))
#                             # bad_list = ''
#                             # [bad_list := bad_list+f'\n<code>{user[0]}</code>, @{user[1]}' for user in bad_users]
#                             #
#                             # try:
#                             #     await bot.edit_message_text('<b>BLACK LIST:</b>\n' + bad_list,
#                             #                                 black_list.chat.id,
#                         #                                     black_list.message_id)
#                         #     except exceptions.TelegramBadRequest:
#                         #         pass
#                         # except exceptions.TelegramBadRequest:
#                         #     print('HERE')
#                 # Now chech user status
#                 if not prem_expires:
#                     # No premium
#                     continue
#                 sec_before_prem_expiry = await calculate_renew_time(
#                     now=now,
#                     future=prem_expires
#                 )
#                 if sec_before_prem_expiry <= 0:
#                     await sql_high_p.set_new_status(client_id, 'user', con=con)
#                     # Если баланс изменился - отправляем уведомление
#                     try:
#                         await bot.send_message(
#                             chat_id=client_id, text=ma_texts['new_status']['user'][lang])
#                     except exceptions.TelegramBadRequest:
#                         pass

async def behind_loop(bot: Bot):
    return None

async def update_users_coins(bot: Bot):
    """
    Constant updating of coins and user status
    """
    now = datetime.datetime.utcnow()
    # Here we create individual connection
    async with aiosqlite.connect(DATABASE) as con:
            dataset = await sql_high_p.get_customers_data(method='data', con=con)

            if not dataset:
                # Dataset is empty yet
                return

            for client in dataset:
                # Формат: (id, 'name'', 'status', date like '199912312359', balance, referrals, 'language)


                client_id = client[0]
                name = client[1]
                status = client[2]
                expiry = client[3]
                balance = client[4]
                referrals = client[5]
                lang = client[6]
                prem_expires = client[9]

                expiry = await get_expiry_date(expiry)
                if now > expiry:
                    default_balance = DEFAULT_BALANCE[status]['general']

                    # Добавим проценты к монетам за каждого реферала
                    ref_reward = round(
                        REFERRAL_RATIO * referrals * default_balance
                    )
                    default_balance += ref_reward

                    # Теперь, если пользователь потратил хоть немного токенов - обновим их
                    new_balance = max(balance, default_balance)

                    update_notice = default_balance > balance

                    await sql_high_p.change_coins_balance(
                        id=client_id, charge=new_balance, method='update', date=now, con=con
                    )
                    if update_notice:
                        markup = None
                        answer_text = ma_texts['auto_update'][lang].format(ref_reward)

                        try:
                            # Если баланс изменился - отправляем уведомление

                            await bot.send_message(
                                chat_id=client_id, text=answer_text, reply_markup=markup, disable_notification=True)
                        except exceptions.TelegramForbiddenError:  # Бот в чс
                            pass

                # Проверим, подписан ли пользователь на канал
                # try:
                #     user_channel_status = (
                #         await bot.get_chat_member(chat_id=TG_RU_CHANNEL_ID, user_id=client_id)
                #     ).status
                #
                #     sub = (user_channel_status not in ('left', 'kicked'))  # True, если подписан
                #
                # except exceptions.TelegramBadRequest as e:
                #     # Пользователь не найден
                #     # Или самого бота нет в канале
                #     sub = False
                # except Exception as e:
                #     # raise
                #     sub = False
                #     await bot.send_message(TG_SUPPORT_ID, "An error occurred while updating the coins:".upper() + e)
                # continue


                # sec_before_update = await calculate_renew_time(
                #     now=now,
                #     future=expiry
                # )
                #
                # if sec_before_update < SLEEP_TIME:  # Время до обновления меньше заданного (или отрицательное)
                #
                #     default_balance = DEFAULT_BALANCE[status]['general']
                #
                #     # Добавим проценты к монетам за каждого реферала
                #     ref_reward = round(
                #         REFERRAL_RATIO * referrals * default_balance
                #     )
                #     default_balance += ref_reward
                #
                #     # Добавим монет за подписку на канал
                #     if sub:
                #         sub_reward = DEFAULT_BALANCE[status]['sub']
                #     else:
                #         sub_reward = 0
                #
                #     default_balance += sub_reward
                #
                #     # Теперь, если пользователь потратил хоть немного токенов - обновим их
                #     new_balance = max(balance, default_balance)
                #
                #     update_notice = default_balance > balance
                #
                #     await sql_high_p.change_coins_balance(
                #         id=client_id, charge=new_balance, method='update', date=now, con=con
                #     )
                #     if update_notice:
                #         markup = None
                #         answer_text = ma_texts['auto_update'][lang].format(ref_reward)
                #         if lang == 'ru':
                #             answer_text += ma_texts['auto_update']['ru_channel_sub'].format(sub_reward)
                #             if not sub:
                #                 markup = subscribe_to_ru_channel_kb
                #         try:
                #             # Если баланс изменился - отправляем уведомление
                #
                #             await bot.send_message(
                #                 chat_id=client_id, text=answer_text, reply_markup=markup)
                #         except exceptions.TelegramForbiddenError:  # Бот в чс
                #             pass

                # Now chech user status
                if not prem_expires:
                    # No premium
                    continue

                prem_expires = await get_expiry_date(prem_expires)

                if prem_expires > now or True:
                    await sql_high_p.set_new_status(client_id, 'user', con=con)
                    # Если баланс изменился - отправляем уведомление
                    try:
                        await bot.send_message(
                            chat_id=client_id, text=ma_texts['new_status']['user'][lang])
                    except exceptions.TelegramBadRequest:
                        pass

