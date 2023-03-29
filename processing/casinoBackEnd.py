# Source: https://gist.github.com/MasterGroosha/963c0a82df348419788065ab229094ac

from typing import List, Tuple
from text_data.message_answers import answers_texts

RESULT = answers_texts['slot_machine']


def get_answer_and_score(dice_value: int) -> int:
    """
    Check for winning
    :param dice_value: значение дайса (число)
    :return: charge (изменение счёта игрока (число))
    Mathematical expectation of game is calculated like:
    (3x8X + 20X + 3x3X - 57X) / 64
    """

    # Совпадающие значения (кроме 777)
    if dice_value in (1, 22, 43):
        result, charge = 'line', 8
    # Начинающиеся с двух семёрок (опять же, не учитываем 777)
    elif dice_value in (16, 32, 48):
        result, charge = 'two_7', 3
    # Джекпот (три семёрки)
    elif dice_value == 64:
        result, charge = 'jackpot', 20
    else:
        result, charge = 'loss', -1
        # result = RESULT['jackpot'], 30 * REWARD_RATIO
    # return 'jackpot', 30*REWARD_RATIO
    return result, charge




def get_combination(value: int) -> List[str]:
    """
    Возвращает то, что было на конкретном дайсе-казино
    :param dice_value: значение дайса (число)
    :return: our combination
    Альтернативный вариант:
        return [casino[(dice_value - 1) // i % 4]for i in (1, 4, 16)]
    """
    #           0       1         2        3
    symbols = ["<b>bar </b>", "🍇", "🍋", "7️⃣"]
    # symbols = ["<b>bar </b>", "🍇", "🍋", "&#x1D7D5; "]
    value -= 1
    result = []
    for _ in range(3):
        result.append(symbols[value % 4])
        value //= 4
    return ''.join(result)


def get_slot_machine_result(value: int, bet: int=10, lang: str='en') -> Tuple[str, int]:
    """
    Function to get slot machine scores
    :param value: combination value
    :param bet: Casino bet. Actually it's a ratio
    :param lang:
    :return: complete answer and coins to charge
    """
    combination = get_combination(value)
    result, charge = get_answer_and_score(value)

    charge *= bet

    # In case we got jackpot the combination won't be put.
    # Formatting doesn't raise Exceptions
    answer = RESULT[result][lang].format(combo=combination, coins=abs(charge))

    return answer, charge
