from payments.config import YOOKASSA_TOKEN

product_description = {
    'coins': {
        'en': '<b>{}</b> of BOTcoins',
        'ru': '<b>{}</b> БОТкоинов'
    },
    'sub': {
        'en': 'sub for <b>{}</b> days',
        'ru': 'Подписка на <b>{}</b> дней'
    },
}

product_synonym = {
        'en': '<b>Purchase item:</b> <i>{}</i>\n',
        'ru': '<b>Продукт:</b> <i>{}</i>\n'
}
go_next = {
    'en': 'Go next to see the price:',
    'ru': 'Перейдите далее, чтобы увидеть стоимость:'
}
payment_method = {
        'en': '<b>Payment method:</b> <i>{}</i>\n',
        'ru': '<b>Способ оплаты:</b> <i>{}</i>\n'
}
price = {
    'en': '<b>Price:</b> <i>{}</i>\n\n',
    'ru': '<b>Стоимость:</b> <i>{}</i>\n\n'
}
currency = {
    'USD': "${}",
    'RUB': "{} ₽",
    'CRYPTO': "${}",
    'BOT': "{} bot"
}
show_requisites = {
        'en': '<b>Use the following payment details for the transfer:</b>\n{}\n\n',
        'ru': '<b>Используйте следующие реквизиты для '
              'перевода:</b>\n{}\n\n'
}
main_market_description = {
        'en': "You can purchase  <b>extra BOTcoins</b> and not "
              "wait for updating.\nAlso you can buy <b>Premium subscription</b>"
              " to have the <b>best user experience</b> and support the developer.",
        'ru': 'Вы можете приобрести <b>дополнительные монеты</b>, '
              'чтобы не ждать их обновления.\n'
              'А ещё можно оформить <b>Premium-подписку</b>: это '
              'сделает использование Бота <b>более '
              'комфортным</b> и поддержит '
              'развитие проекта.'
}

ALL_PAYMENT_METHODS = [
    "RUB_CARD", "RUB_BANK_TRANSFER", 'USD_BANK_TRANSFER',
    "BOT_BALANCE", "CRYPTO_USDT"
]

SUPPORTED_WAYS_TO_PAY = {
    'RUB': {
        'ru': 'RUB',
        'en': 'RUB'
    },
    "USD": {
        'ru': '$USD',
        'en': '$USD'
    },
    "CRYPTO": {
        'ru': 'Криптовалюта',
        'en': 'Pay with crypto'
    },
    "BOT": {
        'ru': "БОТкоины",
        'en': 'BOTcoins'
    }
}

PAYMENT_METHODS_DESCRIPTION = {
    "RUB_CARD": {
            'name': {
                'ru': 'Оплата картой',
                'en': 'Pay by RUB card'
            },
            'description': {
                'ru': 'Оплата банковской картой в рублях. '
                      'Мгновенная обработка платежа.',
                'en': 'Pay by RUB credit card'
            },
            'through_provider': True,
            'provider_token': YOOKASSA_TOKEN
    },
    "RUB_BANK_TRANSFER": {
            'name': {
                'ru': 'Банковский перевод',
                'en': 'RUB bank transfer'
            },
            'description': {
                'ru': 'Банковский перевод по реквизитам. Обработка '
                      'занимает несколько минут, в некоторых случаях '
                      'может занимать несколько часов.',
                'en': 'Банковский перевод по реквизитам'
            },
            'through_provider': False,
            'provider_token': None,
        'requisite': (
            "- <b>Тинькофф</b>:   <u>2200700161841845</u>;\n\n"
            "- <b>СберБанк</b>:   <u>2202202128273756</u>;\n\n"
            "А ещё вы можете воспользоваться кнопкой внизу для "
            "быстрого перевода."
        )
    },
    'USD_BANK_TRANSFER': {
            'name': {
                'ru': 'Bank transfer',
                'en': 'Bank transfer'
            },
            'description': {
                'ru': 'Pay by credit card',
                'en': 'Pay by credit card'
            },
            'through_provider': False,
            'provider_token': None,
            'requisite': (
            "- <b>MasterCard</b>:   <u>5167410245776793</u>;"
        )
    },
    "BOT_BALANCE": {
            'name': {
                'ru': 'Купить за БОТкоины',
                'en': 'Buy with BOTcoins'
            },
            'description': {
                'ru': 'Оплата БОТкоинами с баланса',
                'en': 'You can buy this product with BOTcoins'
            },
            'through_provider': False,
            'provider_token': None
    },
    "CRYPTO_USDT": {
            'name': {
                'ru': 'Купить за USDT',
                'en': 'Pay with USDT'
            },
            'description': {
                'ru': 'Оплата переводом на USDT-кошелёк',
                'en': 'Pay by transfer to USDT wallet'
            },
            'through_provider': False,
            'provider_token': None,
            'requisite': (
                "-<b>TRC20</b>: <code>TT3xwPew8gNJzmErpxjEMN4zHfHqqtjaCe</code>;\n\n"
                "-<b>ERC20</b>: <code>0xa33014d64d458b18d4bc2de549a7931e7514a428</code>;"
            )
    },
}
PAYMENT_CURRENCIES_DESCRIPTION = {
    'BOT': {
            'en': 'You can buy this product with BOTcoins.',
            'ru': 'Этот продукт можно приобрести за БОТкоины.'
    },
    'RUB':  {
            'en': 'Choose payment method:',
            'ru': "Выберите метод оплаты: "
    },
    'USD': {
        'en': 'Choose payment method:',
        'ru': "Выберите метод оплаты: "
    },
    'Crypto': {
        'en': 'Choose payment method:',
        'ru': "Выберите метод оплаты: "
    },
}

PURCHASE_STEPS = {
    'description_of_product': {
        'coins': {
            'en': "More coins - more opportunities! Feel free to chat "
                  "with the Bot on any topic and experiment!",
            'ru': "Больше монет - больше возможностей!\n"
                  "Смело общайтесь с Ботом на любые темы и "
                  "экспериментируйте!"
    },
        'sub': {
            'en': ("Premium subscription expands your possibilities for using the Bot. "
                "<b>Subscription benefits:</b>\n"
                "♦ <i>Much more coins with each update;</i>\n"
                   "<b>more</b> coins for subscribing to a channel;\n "
                   "<b>more</b> coins for each referral;\n"
                "♦ <i>The Bot responds <b>3</b> times faster;</i>\n"
                "♦ <i>The delay between responses is <b>5</b> times less;</i>\n"
                "♦ <i>The maximum answer length is <b>2</b> times longer;</i>\n"
                "♦ <i>During the dialogue, the Bot stores <b>2</b> times more text in memory;</i>"
                "♦ <i><b>Your balance will be updated immediately after you buy subscription</b>.</i>"
                   ),

            'ru': "Premium-подписка расширяет ваши возможности по "
                  "использованию Бота.\n"
                  "<b>Преимущества подписки:</b>\n"
                  "♦<i> намного больше монет при каждом обновлении</i>; <b>больше</b> монет за подписку за канал; <b>больше</b> монет за каждого реферала;\n"
                  # "♦<i> качество изображений <b>1024х1024</b> (без подписки - 512х512)</i>;\n"
                  "♦<i> Бот отвечает в <b>3</b> раза быстрее</i>;\n"
                  "♦<i> Задержка между ответами в <b>5</b> раз меньше</i>;\n"
                  "♦<i> Максимальная длина ответа в <b>2</b> раза больше</i>;\n"
                  "♦<i> Во время диалога Бот хранит в памяти в <b>2</b> раза больше текста</i>;\n"
                  "♦ <i><b>При покупке дата обновления монет сразу сбросится.</b></i>\n"
                  "На какой срок вы хотите оформить подписку?\n"
            },
    },
    'choose_payment_method': {
            'en': 'Choose the payment method:',
            'ru': 'Выберите способ оплаты:'
    },
    'waiting_for_payment': {
            'en': 'The last step: complete the payment.',
            'ru': 'Последний шаг: завершите оплату.'
    },
    'invoice_description': {
        'title': {
            'en': 'Purchasing',
            'ru': 'Оплата'
        },
        'description': {
            'coins': {
            'en': '{} of BOTcoins',
            'ru': '{} БОТкоинов'
            },
            'sub': {
            'en': 'Subscription for {} days',
            'ru': 'Подписка на {} дней'
            },
        }
    },
    'already_has_sub': {
            'en': '<b>You have Premium subscription already!</b> Please, '
                  'wait for your sub expires.',
            'ru': '<b>У вас уже есть Premium-подписка!</b> Пожалуйста, '
                  'дождитесь её окончания.'
    },
    'waiting_for_receipt': {
            'en': '<b>Please make a payment and send a screenshot of '
                  'transaction (receipt) to this chat.</b>',
            'ru': 'Пожалуйста, сделайте перевод и <b>обязательно отправьте сюда '
                  'скриншот транзакции (чек).</b>'
    },
    "complete_the_payment": {
        'en': 'Please complete payment by sending the receipt.',
        'ru': "Пожалуйста, завершите оплату "
                "отправкой чека."

    },
    'insufficient_balance': {
        'en': "Unfortunately, you don't have enough coins to buy that.",
        'ru': "К сожалению, у вас недостаточно монет для покупки."
    },
    'catch_screenshot': {
        'en': "The screenshot is received! The transfer will be processed soon. Thanks!",
        'ru': ("Скриншот получен! Перевод будет обработан в ближайшее время. Спасибо!")
    },
}