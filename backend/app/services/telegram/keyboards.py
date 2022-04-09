from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from . import texts

emoji_num = [
    '0️⃣',
    '1️⃣',
    '2️⃣',
    '3️⃣',
    '4️⃣',
    '5️⃣',
    '6️⃣',
    '7️⃣',
    '8️⃣',
    '9️⃣',
    '🔟',
]

start_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text=texts.start_button_1),
            KeyboardButton(text=texts.start_button_2),
            KeyboardButton(text=texts.start_button_3,
                           request_contact=True)
        ]
    ])

pagination_nav = [
    InlineKeyboardButton(
        text=texts.inline_signup_button_1,
        callback_data='inline_page_left'),
    InlineKeyboardButton(
        text=texts.inline_signup_button_2,
        callback_data='inline_page_center'),
    InlineKeyboardButton(
        text=texts.inline_signup_button_3,
        callback_data='inline_page_right')
]


def signup_detail_nav(
    id: int,
    selected: bool = False,
    notification: bool = False,
) -> InlineKeyboardMarkup:
    """Generate signup detail based on states"""

    keys = [
        InlineKeyboardButton(
            text=texts.inline_detail_action_1,
            callback_data='inline_page_center')
    ]

    if selected:
        keys.append(
            InlineKeyboardButton(
                text=texts.inline_detail_action_3,
                callback_data=f'inline_detail_{id}'))
    else:
        keys.append(
            InlineKeyboardButton(
                text=texts.inline_detail_action_2,
                callback_data=f'inline_detail_{id}'))

    if notification:
        keys.append(
            InlineKeyboardButton(
                text=texts.notify_on,
                callback_data='inline_detail_notify_on'))
    else:
        keys.append(
            InlineKeyboardButton(
                text=texts.notify_off,
                callback_data='inline_detail_notify_off'))

    keyboard = [keys]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def pagination_keyboard(
        options: int,
        cols: int = 5
) -> InlineKeyboardMarkup:
    """Pagination keyboard generator algorithm based on pagination params"""

    # if cols > 8:
    #     # 8 is maximum number of buttons for telegram
    #     cols = 8

    # pages = options // cols
    # remainder = options % cols

    # keyboard = []
    # index = 1
    # while index <= options:
    #     if options <= 10:
    #         i = 0
    #         if index < 5:
    #             i = 1
    #         # keyboard[i].append(
    #         #     InlineKeyboardButton(
    #         #         text=emoji_num[index],
    #         #         callback_data=f'inline_option_{index}'))
    #         keyboard.append(f'inline_option_{index}')
    #     else:
    #         pass
    #     index += 1

    # keyboard.append(pagination_nav)
    # return keyboard

    keyboard = [
        [
            InlineKeyboardButton(
                text=emoji_num[1],
                callback_data='inline_option_1'),
            InlineKeyboardButton(
                text=emoji_num[2],
                callback_data='inline_option_2'),
            InlineKeyboardButton(
                text=emoji_num[3],
                callback_data='inline_option_3'),
            InlineKeyboardButton(
                text=emoji_num[4],
                callback_data='inline_option_4'),
            InlineKeyboardButton(
                text=emoji_num[5],
                callback_data='inline_option_5'),
        ],
        [
            InlineKeyboardButton(
                text=emoji_num[6],
                callback_data='inline_option_6'),
            InlineKeyboardButton(
                text=emoji_num[7],
                callback_data='inline_option_7'),
            InlineKeyboardButton(
                text=emoji_num[8],
                callback_data='inline_option_8'),
            InlineKeyboardButton(
                text=emoji_num[9],
                callback_data='inline_option_9'),
            InlineKeyboardButton(
                text=emoji_num[10],
                callback_data='inline_option_10'),
        ],
        pagination_nav
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
