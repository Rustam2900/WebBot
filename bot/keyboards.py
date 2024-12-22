from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from bot.utils import default_languages


def get_languages(flag="lang"):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="English en", callback_data=f"{flag}_en"),
         InlineKeyboardButton(text="Русский  ru", callback_data=f"{flag}_ru")],
    ])
    return keyboard


def get_main_menu(user_lang):
    main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=default_languages[user_lang]['deposit_money']),
            KeyboardButton(text=default_languages[user_lang]['issuing_money'])
        ],
        [
            KeyboardButton(text=default_languages[user_lang]['settings']),
            KeyboardButton(text=default_languages[user_lang]['statistics'])
        ]

    ], resize_keyboard=True)
    return main_menu_keyboard


def get_admin_menu():
    admin_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="👤Statistika"),
            KeyboardButton(text="✍️ Habar yuborish")
        ],

    ], resize_keyboard=True)
    return admin_menu_keyboard
