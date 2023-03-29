PROPERTIES_DESCRIPTIONS = {
    'digital_art': {
        'en': ("The bot can generate various images, but the most popularity "
               "of neural networks was gained by creating digital art. If this "
               "option is enabled, the bot will always try to draw digital art. If "
               "it's not, the result can be either drawings, sketches, or pictures "
               "very similar to real photos. \nEnabled by default."),

        'ru': "Бот может генерировать различные изображения, "
              "однако самую "
              "большую популярность нейросети обрели, создавая"
              " цифровые арты. Если этот параметр включён, Бот будет"
              " стараться всегда рисовать цифровые арты. Если он "
              "выключен, результатом могут быть рисунки, наброски"
              " и картинки, очень похожие на реальные фото. "
              "\nПо умолчанию включено."
    },
    'temperature': {
        'en': ("The parameter responsible for the bot's creativity while "
               "generating text. The higher the value, the more random each "
               "response will be and the more possible for the Bot to deviate"
               " from the original topic within the response. Low values make "
               "answer more deterministic. Also, high values can increase the "
               "length of the response.\nThe recommended value is 50%, but "
               "feel free to experiment!"),
        'ru': "Параметр, отвечающий за креативность  бота при генерации"
              " текста. Высокое значение делает ответ бота более "
              "рандомным и креативным, а низкое - более стабильным и, "
              "возможно, более релевантным.\nТакже высокие значения "
              "могут повысить длину ответа.\n Рекомендуемое значение - "
              "50%, но вам ничего не мешает поэкспериментировать!"
    },
    'dimension': {
        'en': "Image resolution. The higher the resolution, "
              "the more coins are spent on the generation "
              "of each one, and the higher the image quality.",
        'ru': "Разрешение изображения. Чем выше "
              "разрешение, тем больше монет расходуется"
              " на генерацию и тем выше качество изображения."
    },
    'n_photos': {
        'en': "The number of images that the Bot generates for each "
              "request. \nDefaults to one",
        'ru': "Количество изображений, которое Бот "
              "генерирует за один раз. \nЗначение по умолчанию: 1",
    },
    # 'show_switch': {
    #     'en': "",
    #     'ru': ""
    # },
    'language': {
        'en': "You can change the interface language.",
        'ru': "Вы можете сменить язык интерфейса."
    },
}

PROPERTIES = {
    'en': {
        'switchers': {
            'digital_art': {
                'text': "Digital art",
                'property': "Always draw art"
            },
        },
        'choosers': {
            'dimension': {
                'text': 'Images quality',
                'options':
                    {256: '256', 512: '512', 1024: '1024'}
            },
            'temperature': {
                'text': "Creativity of responses",
                'options':
                # Values to show and values to use inside
                    {
                        1: '10%',
                        5: '25%',
                        10: '50%',
                        15: '75%',
                        20: '100%'
                    }
            },
            'n_photos': {
                'text': "Image variations at a once",
                'options': {1: '1', 2: '2', 3: '3'},
            },
        }

    },
    'ru': {
        'switchers': {
            'digital_art': {
                'text': "Цифровые арты",
                'property': "Всегда рисовать арт"
            },
        # 'show_switch': {
        #     'text': 'Переключатель <Switch>',
        #     'property': 'Показывать в меню'
        # },
        },
        'choosers': {
            'dimension': {
                'text': 'Качество изображенй',
                'options':
                    {256: '256', 512: '512', 1024: '1024'}
            },
            'temperature': {
                'text': "Креативность ответов",
                'options':
                # Values to show and values to use inside
                    {
                        1: '10%',
                        5: '25%',
                        10: '50%',
                        15: '75%',
                        20: '100%'
                    }
            },
            'n_photos': {
                'text': "Количество изображений ",
                'options': {1: '1', 2: '2', 3: '3'},
            },
        }
    }
}

PROPERTIES_DEFAULT_VALUES = {
    'digital_art': 1,
    'temperature': 10,
    # 'temperature': 5,
    'dimension': 512,
    'n_photos': 1,
    # 'show_switch': True
}


LANGUAGES = {
    'en': 'English',
    'ru': 'Русский'
}

SLOT_MACHINE_BETS = [
    0, 10, 100
]
