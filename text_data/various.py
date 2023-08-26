from copy import copy
various_data = {
    'supported languages': {'en': 'English', 'ru': 'Русский'},}

words_to_image = {
    'нарисуй: ', 'можешь нарисовать: ', 'изобрази:', 'нарисуй ',
    'можешь нарисовать ', 'изобрази', 'draw ', 'paint ',
    'can you draw ', 'could you draw ',
}
[words_to_image.add(w.capitalize()) for w in copy(tuple(words_to_image))]
del copy
words_to_image = tuple(words_to_image)
string_for_re_searching = "(" + ')|('.join(words_to_image) + ")"

# emojis = ("🎲", "🎳", "🎯", "🏀", "⚽", "\U0001FA99")
#
# emojis = {
#     'dice': ("🎲", "🎳", "🎯", "🏀", "⚽"),
#     'flip': ("\U0001FA99",)
# }
emojis = {
    'key': (0, 1, 2, 3, 4),
    'emojis': ("🎲", "🎳", "🎯", "🏀", "⚽",),
    'weights': (1,1,1,1,1)
}
links_cover = {
        'en': "link",
        'ru': "ссылка"
    }

expiry_format = {
        'en': "on % at {} UTC",
        'ru': "{} в {} UTC"
    }

# expiry_format = {
#     'coins_update': {
#         'en': "on %d.%m. at %H:%M UTC",
#         'ru': "%d.%m. в %H:%M UTC"
#     },
#     'status_until': {
#         'en': "%H:%M UTC %d.%m",
#         'ru': "%H:%M UTC %d.%m"
#     }
# }

expiry_format = {
    'coins_update': {
        'en': "on %d.%m",
        'ru': "%d.%m"
    },
    'status_until': {
        'en': "%d.%m",
        'ru': "%d.%m"
    }
}