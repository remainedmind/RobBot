from aiogram.filters import BaseFilter, Filter
from aiogram.types import Message
from secret_data import TG_ADMIN_ID

class IsAdmin(Filter):
    """
    Фильтр, определяющий, является ли пользователь админом
    """
    def __init__(self) -> None:
        self.admin_list = (TG_ADMIN_ID, )

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_list
