import json
PROMO_FILE = 'constants/promo.json'


async def get_promos() -> dict:
    with open(PROMO_FILE, encoding='UTF-8') as json_file:
        data = json.load(json_file)
    return data


async def rewrite_promos(data):
    with open(PROMO_FILE, 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file)
    return data