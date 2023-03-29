import json
import pickle
PROMO_FILE = 'promo.json'


async def get_promos() -> dict:
    with open(PROMO_FILE) as json_file:
        data = json.load(json_file)
    return data


async def rewrite_promos(data):
    with open(PROMO_FILE, 'w') as json_file:
        json.dump(data, json_file)
    return data