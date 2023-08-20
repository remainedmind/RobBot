from aiogram import html, md

answers_texts = {
    'switch': {
        'en': "Your command menu was changed to the new version.",
        'ru': "Ваше меню изменено. Теперь там только актуальные команды."
    },
    'start': {
        'new_user': {
            'en': "Hello, <b>{}</b>!\nPlease click <b><i>/start</i></b> to run the Bot. ",
            'ru': "Привет, <b>{}</b>! Пожалуйста, нажми <b><i>/start</i></b> для запуска бота."
        },
        'empty_username': {
            'en': "human",
            'ru': "человек"
        },
        'hello': {
            'en': "What's up, <b>{}</b>!\nReady to start?",
            'ru': "Приветствую, <b>{}</b>! Я готов к работе, а ты?"
        },
        'group': {
            'en': ("Now Bot is available for use! Please open <b>private chat"
                  "</b> with Bot to see our welcome message!"),
            'ru': ("Бот доступен для использования! Отправили "
                   "приветственное сообщение в ваш <b>личный чат</b>!")
            },
        'failed': {
            'en': "Please start the Bot in a <b>private dialogue</b>.",
            'ru': "Пожалуйста, запустите Бота в <b>личном чате</b>."
            },
        'restart': {
            'en': "Please start the Bot by clicking <b>/start</b> and the button.",
            'ru': "Пожалуйста, запустите Бота, нажав в <b>/start</b> и кнопку запуска."
        },
        'private': {
            'en': ("I'm smart chat bot based on GPT. I can "
                "<i>answer questions</i>, <i>write articles and code</i>, <i>draw images</i> "
                "and <i>recognize voice messages</i>. Try to send something to me! Every question"
                " answer spends  <b>BOTcoins </b>. Amount of coins"
                " can be seen by clicking <b><i>/account</i></b>.\n"
                "\nClick <b><i>/help</i></b> for more information"
                ),
            'ru': ("Я - умный чат-бот на основе <b>Искусственного "
                   "интеллекта</b>. Я умею <i>отвечать на вопросы</i>, <i>писать"
                   " статьи</i>, <i>создавать изображения</i> и <i>распознавать текст"
                   " голосовых сообщений</i>. Напишите мне что "
                   "угодно!\n"
                   "Мои ответы расходуют монеты - <b>"
                   "БОТкоины</b>. Дату обновления БОТкоинов "
                   "можно увидеть с помощью команды <b><i>"
                   "/account</i></b>.\nЧем объёмнее вопрос и ответ,"
                   " тем больше тратится монет.\nДля подробной "
                   "информации нажмите <b><i>/help</i></b>.\n"
                    "А ещё меня можно использовать в <b>групповых чатах</b>."
                )
        },
    },
    'help': {
            'en': (
                "📖 <b>HANDBOOK</b> 📖\n\n"
                "I am a <b>chatbot</b> powered by AI models. I'm able "
                "to\n1) <i>answer questions</i>;\n"
                "2) <i>write articles and code</i>;\n"
                "3) <i>draw images</i>;\n"
                "4) <i>recognize voice messages</i>.\n"
                "Try to send something to "
                "me!\n<b><i>Commands:</i></b>\n"
               "/help - see that message again;\n" 
               f"/ask {html.quote('<message text>')} -  ask me in a group chat;\n"
               f"/image - to create an image from textual descriptions. It "
               f"costs from 600 BOTcoins;\n"
               "/account - see your <b>BOTcoins</b> balance;\n"
              "/dice - play roulette without spending coins and "
                   "have a little fun (you will "
                   "see this command only in a group chat);\n"
                "\nStill have questions? Write to admin using following format:"
                   f"\n<i>Admin, </i> {html.quote('<message text>')}. "
                   "✏ A comma is required, you can attach a screenshot and "
                "you can <b>cancel this action</b>."
               "\nSee more commands in your <b>pop up menu</b>!"),
            'ru': ("📖 <b>КАК МЕНЯ ИСПОЛЬЗОВАТЬ</b> 📖\n\n"
                   "Я - умный чат-бот с ИИ под капотом. Я могу:\n"
                   "1) <i>ответить на любой вопрос</i>;\n"
                   "2) <i>написать большой текст или код</i>;\n"
                   "3) <i>нарисовать арт</i>;\n"
                   "4) <i>расшифровать голосовое сообщение</i>;\n"
                   "5) <i>просто повеселить вас</i>.\n"
                   "\nВсё это (кроме веселья) требует вычислительных затрат, поэтому расходует монеты - "
               "<b>БОТкоины</b>, которые обновляются со временем.\n"
               "Чем объёмнее вопрос и ответ, тем больше тратится монет.\n"
              "<b><i>Команды:</i></b>"
                   "\n/main - главное меню;"
                   "\n/help - увидеть это сообщение снова;\n"
               "/image - создать изображение по описанию. Одно "
               "изображение стоит от 600 БОТкоинов;"
               f"\n/ask {html.quote('<текст сообщения>')} - задать вопрос <b>боту</b> в <i>беседе</i>;\n"
               "/dice - испытать судьбу и немного развлечься "
                   "(<i>не расходует монеты</i>; команда "
                   "отображается только в групповых чатах);\n"
                   "\nОстались вопросы? Напишите администратору, "
                   "используя следующий формат:\n"
              f"<i>Админ, </i> {html.quote('<текст сообщения>')}. "
                   f"✏ Запятая обязательна; сообщение отправляется <b>не "
                   f"сразу</b>; можно прикрепить скриншот."
               "\n\nОстальные команды вы можете увидеть во <b>всплывающем меню</b>!"
               )
    },
    'main': {
        'en': "🔷 <b>MAIN PAGE</b> 🔷",
        'ru': "🔷 <b>ГЛАВНОЕ МЕНЮ</b> 🔷"
    },
    'settings': {
        'en': "⚙ <b>SETTINGS</b> ⚙\n\n",
        'ru': "⚙ <b>НАСТРОЙКИ</b> ⚙\n\n"
    },
    'settings_main': {
        'en': "Choose the option:",
        'ru': "Выберите параметр:"
    },
    'account': {
        'en': ("🔷 <b>MY ACCOUNT</b> 🔷\n"
               "\n🔸 Biological species: <b>Homo sapiens</b>;"
               "\n🔸 Your status is: <b>{status}</b>;"
               "\n🔸 Your balance is <b>{balance}</b> <b>BOTcoins</b>;"
               "\n🔸 Your balance will be updated:\n     <b>{expiry}</b>;"
               "\n🔸 Your referrals: <b>{referrals}</b>;"
               "\n🔸 The total amount of spent coins: <b>{total}</b>."),
        'ru': ("🔷 <b>МОЙ АККАУНТ</b> 🔷\n"
               "\n🔸 Вид: <b>человек разумный</b>;"
               "\n🔸 Ваш статус: <b>{status}</b>;"
               "\n🔸 Баланс: <b>{balance} БОТкоинов</b>;"
               "\n🔸 Обновление баланса:\n   <b>{expiry}</b>;"
               "\n🔸 Ваши рефералы: <b>{referrals}</b>;"
               "\n🔸 Потрачено монет за всё время: <b>{total}</b>.")
    },
    'market': {
        'en': "🛍 <b>SHOP</b> 🛍\n\n",
        'ru': "🛍 <b>МАГАЗИН</b> 🛍\n\n"
    },
    'premium_additional_phrase':{
        'en': " until {}",
        'ru': " до {}"
    },

    'answering': {
        'text':
            {
            'en': ["<b>Reading your question carefully</b>...", "<b>Trying to realize</b>...", "<b>Creating an answer</b>..."],
            'ru': ["<b>Внимательно читаем вопрос</b>...", "<b>Собираем мысли в кучу</b>...","<b>Генерируем ответ</b>..."]
            },
        'photo':
            {
            'en': ["What do you want to see? <b>Describe the desired image.</b>", "<b>Okay, where are my paints and brushes</b>...","<b>Generating an image</b>...", "<b>The final touch</b>...", "<b>That's how I imagine it:</b>"],
            'ru': ["Что для вас нарисовать? <b>Опишите желаемое изображение.</b>", "<b>Достаём кисточки и краски</b>...","<b>Генерируем изображение</b>...", "<b>Последний штрих</b>...", "Я художник, я вижу <b>так</b>:"]
            },
        'voice':
            {
            'en': ["<b>Okay, where are my headphones</b>...", "<b>Listening carefully</b>...", "<b>Almost ready</b>...", "*That's what I heard:*\n\n `{}`\n\n *Would you like to ask that?*"],
            'ru': ["<b>Так, где мои наушники</b>...", "<b>Слушаю</b>...","<b>Почти готово</b>...", "*Вот, что мне удалось распознать:*\n\n `{}`\n\n *Вы хотите спросить меня об этом?*"]
            },
        'unknown_text_error': {
            'en': "There was an error while processing your question  :(\nIt happens due to a high server load.\nLet's try again!",
            'ru': "Из-за высокой нагрузки на сервер у нас не получилось обработать ваш запрос :(\nТакое бывает - просто попробуйте ещё раз!"
        },
        'empty command': {
            'en': "Message text after command was expected. Try again or use /help.",
            'ru': f"После команды должен следовать текст сообщения. \nПопробуйте ещё раз или нажмите /help."
        },
        'empty_voice': {
            'en': "The message wasn't recognized: no word was caught.\nPlease try again.",
            'ru': "Сообщение не было распознано: не обнаружено ни одного слова. Попробуйте ещё раз!"
        },
        'unknown_voice_error': {
            'en': "An error occurred while processing the voice. Please try again.",
            'ru': "Произошла ошибка при обработке голосового сообщения.\n"
                  "Пожалуйста, попробуйте ещё раз!"
        },
        'unknown_drawing_error': {
            'en': "An error occurred while drawing. Please try again.",
            'ru': "При генерации изображения произошла ошибка "
                  "на сервере. Пожалуйста, попробуйте ещё раз!"
        },
        'voice_is_too_long': {
            'en': "Message is too long, we can't process it",
            'ru': "Сообщение слишком длинное, мы не можем обработать его."
        },
        'dialogue_limit': {
            'en': "Dialogue is too long, some of previous text was deleted from memory.",
            'ru': "Диалог оказался слишком длинным: часть предыдущих "
                  "сообщений была удалена из памяти."
        },
        'error_dut_to_dialogue_limit': {
            'en': "We have error: dialogue is too long. Please "
                  "reset it manually.",
            'ru': "Произошла ошибка: диалог оказался слишком "
                  "длинным. Пожалуйста, сбросьте его вручную."
        },
        'error_with_voice_answering': {
            'en': "Sorry, we can't process it. Copy and ask manually, please.",
            'ru': "ERROR"
        },
        'empty_ask': {
            'en': "There was an error while processing your question  :(\nIt happens due to a high server load.\nLet's try again!",
            'ru': "Из-за высокой нагрузки на сервер у нас не получилось обработать ваш запрос :(\nТакое бывает - просто попробуйте ещё раз!"
        },
    },
    'conversation': {
        'start': {
            'en': "The dialogue has been started",
            'ru':  "Начали диалог. Теперь я запоминаю все сообщения."
        },
        'reset': {
            'en': "The dialogue has been reset",
            'ru':  "Диалог сброшен. Старые сообщения удалены из памяти. "
        },
        'stop': {
            'en': "The dialogue has been stopped",
            'ru':  "Диалог остановлен."
        }
    },
    'slot_machine': {
        'main': {
            'en': ("🎰 <b>SLOT MACHINE</b> 🎰"),
            'ru': ("🎰 <b>СЛОТ-МАШИНА</b> 🎰")
        },
        'rules': {
            'en': ("🎰 <b>SLOT MACHINE</b> 🎰\n\n"
                   "Result is generated independently (on the Telegram server); \n"
                    "- <i>Three fruits or bar</i> - prize is <b>8X</b> from the bet;\n"
                    "- <i>Three sevens</i> - <b>jackpot</b>, prize is <b>20 X</b> from the bet;\n"
                    "- <i>The bet can be changed.</i>"),
            'ru':  ("🎰 <b>ИГРОВОЙ АВТОМАТ</b> 🎰\n\n"
                    "Генерация результата - на сервере Telegram (независимая сторона);\n"
                    "- <i>Три фрукта или bar</i> - выигрыш <b>8Х</b> от ставки;\n"
                    "- <i>Три семёрки</i> - <b>джекпот</b>, выигрыш <b>20Х</b> от ставки;\n"
                    "- <i>Ставку можно изменить.</i>")
        },
        'bets': {
            'en': ("🎰 <b>SLOT MACHINE</b> 🎰\n\nThe winnings are proportional to your bet. Set it up:"),
            'ru': ("🎰 <b>СЛОТ-МАШИНА</b> 🎰\n\nВыигрыш пропорционален ставке. Выберите ставку:")
        },
        'loss': {
            'en': ("Combination: {combo}\nYou'll get it next time :(\n<b>{coins}</b> BOTcoins have been charged from balance."),
            'ru':  ("Комбинация: {combo}\nПовезёт в другой раз :(\n<b>{coins}</b> БОТкоинов списаны с баланса.")
        },
        'line': {
            'en': ("Combination: {combo}\n<b>You won</b>! Сongratulations!\n<b>{coins}</b> BOTcoins have been added to balance. 💸"),
            'ru': ("Комбинация: {combo}\n<b>Выигрыш</b>! Поздравляю!\n<b>{coins}</b> БОТкоинов начислены на баланс. 💸")
        },
        'two_7': {
            'en': ("Combination: {combo}\nIt was so close! <b>Consolation Prize</b>:\n<b>{coins}</b> BOTcoins have been added to balance. 💸"),
            'ru': ("Комбинация: {combo}\nОчень близко! <b>Утешительный приз</b>:\n<b>{coins}</b> БОТкоинов начислены на баланс. 💸")
        },
        'jackpot': {
            'en': ("✨<b>JACKPOT</b>✨! I wish I was as lucky as you!\n<b>{coins}</b> BOTcoins have been added to balance. 💸"),
            'ru': ("✨<b>ДЖЕКПОТ</b>✨! Компьютер никогда не заменит твоё везение! \n<b>{coins}</b> БОТкоинов начислены на баланс. 💸")
        },
    },

    'throttling': {
            'en': "Please wait <b>{}</b> seconds more.",
            'ru': "Пожалуйста, подождите ещё <b>{}</b> секунд."
    },
    'unexpected_image': {
        'en': "Sorry, I am unable to process this file. Please make sure your actions are correct. \n"
              "Need help? Write '<code>Admin, </code>' and your message",
        'ru': "К сожалению, я не могу обработать этот файл. Убедитесь, что вы всё делаете правильно.\n"
              "Нужна помощь? Напишите <code>Админ, </code> и ваше сообщение."
    },



    'auto_update': {
        'en':
            ("<b>Your BOTcoin balance has just been updated!</b> Have fun!\n"
            "Extra <b>BOTcoins</b> within the referral program: <b>{}</b>."),
        'ru':
            ("<b>Ваш баланс БОТкоинов обновлён!</b> Веселитесь!\n"
            "Бонусы в рамках реферальной программы: <b>{} БОТкоинов</b>."),
        'ru_channel_sub': "\nБонус за подписку на канал: <b>{} БОТкоинов</b>."
    },

    'insufficient_balance': {
        'zero':
            {
            'en': "Unfortunately, you have run out of coins. The balance will be updated <b>{}</b>",
            'ru': "К сожалению, у вас закончились монеты. Баланс будет обновлён <b>{}</b>"
            },
        'lack':
            {
            'en': "Unfortunately, you don't have enough coins. The balance will be updated <b>{}</b>",
            'ru': "К сожалению, у вас недостаточно монет. Баланс будет обновлён <b>{}</b>"
            },
    },
    'got_coins': {
        'en': "You've just got BOTcoins: <b>{}</b>. Thanks for using Rob!",
        'ru': "Ваш баланс пополнен на <b>{}</b> БОТкоинов. Спасибо за использование бота!"
    },
    'payment_failed': {
        'en': "Something went wrong :(\n"
              "If funds were deducted from your account, please "
              "<b>contact the administrator</b>. For more "
              "information, visit <b>/help</b>.",
        'ru': "Что-то пошло не так :(\n"
              "Если средства были списаны с вашего счёта, пожалуйста,"
              " <b>свяжитесь с администратором</b>; подробнее - "
              "<b>/help</b>."
    },
    'new_status': {
        'premium':
            {
                'en': "Your status has just been changed to <b>PREMIUM</b>. Thanks for using Rob! Your balance will be updated soon.",
                'ru': "Ваш статус изменён на <b>PREMIUM</b>. Спасибо за использование бота! Ваш баланс будет обновлён очень скоро."
            },
        'user':
            {
                'en': "Your premium account status has expired. Your status is <b>USER</b> now.",
                'ru': "Срок действия premium-аккаунта истёк. Статус изменён на <b>USER</b>."
            }
    },



    'referral': {
        'message': {
            'en': ("That's your referral link:\n<i>{}</i>\nReferral program bonuses:\n"
                  "♦<i> instant bonus for referral</i>;\n"
                  "♦<i> extra BOTcoins at every update</i>;\n"
                  "♦<i> more BOTcoins when buying if you have referrals</i>;\n"
                  "♦<i> bonus when referral buys BOTcoins</i>: if your"
                  " referral will buy coins, you will receive a percentage of his purchase."
                  "\nUse the <b>button</b> below to quickly send link to Telegram chat.\n"
                  " ‼ we advise you to erase the nickname in the invitation letter and leave only the link! "
                  "Telegram obliges us to insert a nickname in the message, but referrals will be counted <b>only by the link</b>!"),
            'ru': ("Ваша реферальная ссылка:\n<i>{}</i>\n"
                  "<b>Бонусы реферальной программы</b>:\n"
                  "♦<i> мгновенный бонус за реферала</i>;\n♦<i> бонус при каждом обновлении БОТкоинов</i>;\n"
                  "♦<i> больше БОТкоинов при покупке, если у вас есть рефералы</i>;\n"
                  "♦<i> бонус при покупке монет вашим рефералом</i>: если ваш"
                  " реферал купит монеты, вы получите процент от его покупки."
                  "\nИспользуйте <b>кнопку</b> ниже для быстрой отправки"
                  " в Telegram.\n"
                  "‼ советуем стереть никнейм в пригласительном письме и оставить только ссылку!"
                   "\nTelegram обязывает вставлять никнейм в сообщение, но рефералы засчитаются <b>только по ссылке</b>!"
            )
        },
        'referral_text': {
            'en': "⬅ delete this nickname, leave only link below⬇:\n{}",
            'ru': "⬅  удалите никнейм слева; оставьте ссылку внизу⬇:\n{}"
        },
        'new_referral': {
        'en': "Your referral has registered. You've just got <b>{} BOTcoins</b>! Isn't that wonderful?",
        'ru': "Ваш реферал зарегистрировался. Ваш баланс пополнен на <b>{} БОТкоинов</b>! Ну разве это не прекрасно?"
    },
    },

    'feedback': {
        'show_message': {
        'en': "<b>Admin will see following message:</b>",
        'ru': "<b>Администратор увидит следующее сообщение:</b>"
    },
        'empty': {
            'en': "Add the text after '<i>Admin, </i>'",
            'ru': "После '<i>Админ, </i>' добавьте текст сообщения."
        },
        'was_sent_to_admin': {
        'en': "Message was sent to admin successfully. Thanks!",
        'ru': "Сообщение успешно отправлено администратору. Спасибо!"
    },

        'message_from_admin': {
        'en': "<b>New message from Admin</b>:\n{}",
        'ru': "<b>Новое сообщение от Администратора</b>:\n{}"
    },
        # 'message_from_admin': {
        #     'en': "New message from Admin:\n{}",
        #     'ru': "New message from Admin:\n{}"
        # },
        'message_from_user': (
            "New feedback message from @{}.\nID: <code>{}</code>\nStatus: {}.\nBalance: {}\nReferrals: {}."
        ),
        'show_message_for_user': "<b>OK, send me the message to forward.</b>",
        'message_for_user': "<b>User will see the message:</b>",
        'was_sent_to_user':  "<b>Message was sent to user successfully.</b>",
    },

    'update_done': {
            'en': ("Hi, {}! <b>WE HAVE AN UPDATE</b>! We made the Bot a little better. "
                    "<b>Before using, please restart the Bot by "
                    "pressing the command <i>/start</i></b>."),
            'ru': "Привет, {}! <b>У НАС ОБНОВЛЕНИЕ</b>! Мы сделали Бота немного лучше. "
                  "<b>Перед использованием, пожалуйста, перезапустите Бота, "
                  "нажав команду <i>/start</i></b>."
            },
    'update_is_going': {
            'en': "Hi, {}! <b>We are updating our Bot right now to make it better</b>. Please come back later.",
            'ru': "Привет, {}! В данный момент мы обновляем Бота, чтобы сделать его"
                  "ещё лучше. Пожалуйста, попробуйте позже"
    },
    'promocode':{
        True: {  # Success
            'en': "Promo code applied! Bonuses have been credited.",
            'ru': "Промокод применён! Бонусы были начислены."
        },
        False: {  # Failed
            'en': "Unfortunately, the promo code is invalid.",
            'ru': "К сожалению, промокод недействителен."
        }
    }
}
admin_command_answers = {
    'info_about_user':  ("Human @{nickname}.\nID: <code>{id}</code>\nStatus: {status};\n"
                         "Balance: {balance};\n"
                         "Referrals: {referrals};\n"
                         "Referrer: {referrer};\n"
                         "Language: {language};\n"
                         "Premium until: {prem_expires}"),
    'payment_from':  (
        "NEW PAYMENT FROM @{nickname}\."
        "\nID: <code>{id}</code>\nStatus: <b>{status}</b>;\n"
                         "Balance: {balance};\n"
                         "Referrals: {referrals};\n"
                         "Referrer: {referrer};\n"
                         "Language: {language};\n"
                         "Premium until: {prem_expires}\n"
        "PURCHASE: {payment}"
    ),
    'amout_of_users': ('Total amount of users: <b>{}</b>'),
    'new_status': ("Client status was succesfully changed to: <b>{}</b>"),
    'new_balance': ("Client's balance was succesfully charged for: <b>{}</b>"),
    'spam_first': ("OK, send me the message to spam"),
    "spam_second": ("USERS will see:\n"),
    "spam_third": ("To whom you want to send it?"),
    "spam_final": ("Spam was sent successfully!")
}
