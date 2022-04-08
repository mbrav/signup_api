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


signup_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
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
        [
            InlineKeyboardButton(
                text=texts.signup_inline_button_1,
                callback_data='inline_page_left'),
            InlineKeyboardButton(
                text=texts.signup_inline_button_2,
                callback_data='inline_page_center'),
            InlineKeyboardButton(
                text=texts.signup_inline_button_3,
                callback_data='inline_page_right')
        ]
    ])
