from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from . import texts

start_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text=texts.start_button_1),
            KeyboardButton(text=texts.start_button_2),
            KeyboardButton(text=texts.start_button_3,
                           request_contact=True)
        ]
    ])
