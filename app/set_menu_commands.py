# from aiogram.methods.set_my_commands import SetMyCommands

from aiogram.methods import SetMyCommands

from aiogram import Bot, Dispatcher, exceptions, types
from aiogram.fsm.context import FSMContext

from text_data.commands import commands
from secret_data import TG_ADMIN_ID

from aiogram.types.bot_command_scope_chat import BotCommandScope
from aiogram.types.bot_command_scope_default import BotCommandScopeDefault
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
# from aiogram.types.bot_command_scope_default import BotCommandScope

async def set_default_command_menu(bot: Bot, langs=('ru', )) -> bool:
    """
    Function to set up default command when starting the Bot
    :param bot: Bot
    :param langs: All supported languages
    :return: True on success
    """

    for lang in langs:
        # Set up for supported languages
        private_coms = commands['user']['private'][lang]
        group_coms = commands['user']['group'][lang]
        await bot.set_my_commands(scope=BotCommandScope(type='all_private_chats'), language_code=lang, commands=private_coms),
        await bot.set_my_commands(scope=BotCommandScope(type='all_group_chats'), language_code=lang, commands=group_coms)

    def_private_coms = commands['user']['private']['en']
    def_group_coms = commands['user']['group']['en']

    # Default menu for other languages is english menu
    await bot.set_my_commands(scope=BotCommandScope(type='all_private_chats'),
                              commands=def_private_coms),
    await bot.set_my_commands(scope=BotCommandScope(type='all_group_chats'), commands=def_group_coms)
    return True


async def set_personal_menu_commands(chat_id, user_id, lang, bot: Bot):
    """

    """
    key = 'admin' if user_id == TG_ADMIN_ID else 'user'
    if chat_id == user_id:
        kwargs = {
            'type': 'chat', 'chat_id': chat_id}
        cmnds = commands[key]['private'][lang]
    else:
        # group chat
        kwargs = {
            'type': 'chat_member', 'chat_id': chat_id, 'user_id': user_id
        }
        cmnds = commands[key]['group'][lang]
        await bot.set_my_commands(scope=BotCommandScope(**kwargs), commands=cmnds)

        # And we anyway change private chat menu
        kwargs = {
            'type': 'chat', 'chat_id': user_id}
        cmnds = commands[key]['private'][lang]


    await bot.set_my_commands(scope=BotCommandScope(**kwargs), commands=cmnds)



