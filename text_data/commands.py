from aiogram.types.bot_command import BotCommand


commands_text = dict(
        admin = {  # ADMIN of BOT
            'private': {
                'en': [
                    ('main', 'Main page'),
                    # ('switch', 'Switch language'),
                    ('image', 'Create image'),
                    ('account', 'Account details'),
                    ('reset', "Reset chat"),
                    ('spam', "Send spam"),
                    ('myusers', 'My users'),
                    ('manage', 'Manage user'),
                    ('answer', "Message to user"),
                ],
                'ru': [
                    ('main', 'На главную'),
                    # ('switch', 'Сменить язык'),
                    ('image', 'Создать изображение'),
                    ('account', 'Мой аккаунт'),
                    ('spam', "Рассылка"),
                    ('myusers', 'Пользователи'),
                    ('manage', 'Manage user'),
                    ('answer', "Message to user"),
                    ]
                },
            'group': {
                'en': [
                    ('ask', 'Ask bot'),
                    ('main', 'Main page'),
                    # ('switch', 'Switch language'),
                    ('image', 'Create image'),
                    ('account', 'Account details'),
                    ('reset', "Reset chat"),
                    ('dice', 'Make a dice'),
                    # ('spam', "Send ads"),
                    ('myusers', 'My users'),
                    ('manage', 'Manage user'),
                    ('answer', "Message to user"),
                ],
                'ru': [
                    ('ask', 'Спросить бота'),
                    ('main', 'Главное меню'),
                    # ('switch', 'Сменить язык'),
                    ('image', 'Создать изображение'),
                    ('account', 'Мой аккаунт'),
                    ('reset', "Сбросить диалог"),
                    ('dice', 'Рулетка'),
                    # ('spam', "Send ads"),
                    ('myusers', 'My users'),
                    ('manage', 'Manage user'),
                    ('answer', "Message to user"),
                ]
            }
        },
        user = { # USERS
            'private':  {
                'en': [
                    ('main', 'Main page'),
                    ('image', 'Create image'),
                    ('account', 'Account details'),
                    ('reset', "Reset chat"),
                    ('help', 'See handbook'),
                ],
                'ru': [
                    ('main', 'На главную'),
                    ('image', 'Создать изображение'),
                    ('account', 'Мой аккаунт'),
                    ('reset', "Сбросить диалог"),
                    ('help', 'Справка'),
                ]
            },
            'group':  {  # USERS
                'en': [
                    ('ask', 'Ask bot'),
                    ('main', 'Main page'),
                    ('image', 'Create image'),
                    ('reset', "Reset chat"),
                    ('account', 'Account details'),
                    ('dice', 'Make a dice'),
                    ('help', 'See handbook'),
                ],
                'ru': [
                    ('ask', 'Спросить бота'),
                    ('main', 'Главное меню'),
                    ('image', 'Создать изображение'),
                    ('reset', "Сбросить диалог"),
                    ('account', 'Мой аккаунт'),
                    ('dice', 'Рулетка'),
                    ('help', 'Справка'),
                ]
            }
        }
)


commands = dict(
        admin = {  # ADMIN of BOT
            'private':  {
            'en': [
                BotCommand(command=c, description=d) for c, d in commands_text['admin']['private']['en']
            ],
            'ru': [
                BotCommand(command=c, description=d) for c, d in commands_text['admin']['private']['ru']
            ]
        },
            'group':  {
            'en': [
                BotCommand(command=c, description=d) for c, d in commands_text['admin']['group']['en']
            ],
            'ru': [
                BotCommand(command=c, description=d) for c, d in commands_text['admin']['group']['ru']
            ]
            }
        },
        user =  {
            'private':  {
                'en': [
                    BotCommand(command=c, description=d) for c, d in commands_text['user']['private']['en']
                ],
                'ru': [
                    BotCommand(command=c, description=d) for c, d in commands_text['user']['private']['ru']
                ]
        },
            'group':  {
                'en': [
                    BotCommand(command=c, description=d) for c, d in commands_text['user']['group']['en']
                ],
                'ru': [
                    BotCommand(command=c, description=d) for c, d in commands_text['user']['group']['ru']
                ]
            }
        }
)