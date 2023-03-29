from aiogram.filters import Filter
from aiogram.types import Message
from processing.PromoCodeProcessing import get_promos, rewrite_promos


class IsPromocode(Filter):
    """
    Фильтр для использования промокода. Проверяет соответствие
    текста промокода и количество доступных использований.
    """
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool | dict:
        validity = False
        bonus = 0
        id = message.from_user.id
        promo = await get_promos()
        text = message.text
        if text in promo.keys():
            if promo[message.text]['usage_limit'] > 0:
                if not id in promo[text]['used_by']:
                    # Уменьшаем количество использований
                    promo[message.text]['usage_limit'] -= 1
                    promo[message.text]['used_by'].append(id)
                    validity = True
                    bonus = promo[message.text]['bonus']
                    await rewrite_promos(promo)
            return {'validity': validity, 'bonus': bonus}
        return False