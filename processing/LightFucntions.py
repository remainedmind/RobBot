import random as rd
from text_data.various import emojis

async def get_emoji(seed) -> str:
    rd.seed(seed)  # Initializing the seed for random generation
    choices: dict = emojis
    key = rd.choices(population=choices['key'], weights=choices['weights'], k=1)[0]
    return choices['emojis'][key], choices['type'][key]