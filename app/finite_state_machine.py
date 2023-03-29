from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    need_to_unblock_bot = State()
    main = State()
    image_generation = State()
    answer2user = State()
    coins_giving = State()
    sending_receipt = State()
    spamming = State()