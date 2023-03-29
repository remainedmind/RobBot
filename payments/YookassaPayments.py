YOOKASSA_KEY='live_BUt8AKQoFnParM-nNfyUKQtRYQkyM_ww0HtSUaaFG4c'
SHOP_ID=203162



import requests

from yookassa import Payment, Configuration

Configuration.account_id = SHOP_ID
Configuration.secret_key = YOOKASSA_KEY

payment = Payment.create({
    "amount": {
        "value": "80.00",
        "currency": "RUB"
    },
    "payment_method_data": {
        "type": "bank_card"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://t.me/AI_rob_bot"
    },
    "capture": True,
    "description": "Заказ №72"
})
print(payment.json())