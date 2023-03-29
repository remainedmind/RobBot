


from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.filters.command import CommandStart, Command
from aiogram.types import ChatMemberUpdated, Message
from aiogram.methods.send_message import SendMessage

from secret_data import TG_SUPPORT_ID

router = Router()
router.my_chat_member.filter(F.chat.type == "private")
router.message.filter(F.chat.type == "private")



@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated):
    user_id= event.from_user.id
    user_nickname = event.from_user.username
    await SendMessage(
        chat_id=TG_SUPPORT_ID,
        text=f'❗️Внимание\! Этот кожаный мешок с костями заблокировал бота:\n'
             f'@{user_nickname}\;\nID: `{user_id}`',
        parse_mode='MarkdownV2'
    )


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated):
    user_id = event.from_user.id
    user_nickname = event.from_user.username
    await SendMessage(
        chat_id=TG_SUPPORT_ID,
        text=f'❗️Внимание\! Этот кусок мяса переобулся и разблокировал бота:\n'
             f'@{user_nickname}\;\nID: `{user_id}`',
        parse_mode='MarkdownV2'
    )