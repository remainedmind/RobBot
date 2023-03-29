from datetime import datetime, timedelta


from const import UPDATE_TIME, INSTANT_REFERRAL_REWARD, PREMIUM_DURATION




async def set_expiry_date(date: datetime, extra_time: dict) -> str:
    """ Transform datetimee to string"""

    date = date + timedelta(**extra_time)
    date = date.strftime("%Y%m%d%H%M")
    return date

async def get_expiry_date(date: str) -> datetime:
    """ Transform string to datetime """
    date = datetime.strptime(date, "%Y%m%d%H%M")
    # datetime.combine()
    return date


async def calculate_renew_time(now: datetime, future: str) -> int:
    """
    Расчёт времени до обновления монет
    :param now:
    :param future:
    :return:
    """
    # Преобразуем в тип datetime
    future = await get_expiry_date(future)
    # Cчитаем разницу
    return (future - now).total_seconds()

