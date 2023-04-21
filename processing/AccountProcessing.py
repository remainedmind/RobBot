from processing.SQL_processingg import SQL_high_level_processing as sql_high_p
from processing import timeProcessing as timep

from text_data.message_answers import answers_texts as ma_texts
from text_data.various import expiry_format

async def get_date_of_coins_updating(lang, expiry: str) -> str:

    expiry = await timep.get_expiry_date(expiry)
    expiry = expiry.strftime(expiry_format['coins_update'][lang])
    return expiry


async def get_account_details(id, lang) -> str:

    info = await sql_high_p.get_user_info_quickly(id)

    expiry = await timep.get_expiry_date(info['expiry'])
    info['expiry'] = expiry.strftime(expiry_format['coins_update'][lang])

    status = info['status'].upper()
    if status != 'USER':
        premium_expiry = await timep.get_expiry_date(info['prem_expires'])
        premium_expiry = premium_expiry.strftime(expiry_format['status_until'][lang])
        status += ma_texts['premium_additional_phrase'][lang].format(premium_expiry)
    info['status'] = status
    return ma_texts['account'][lang].format(**info)
