from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

r_kb_b = [
    [KeyboardButton(text='Сегодня')],
    [KeyboardButton(text='Вчера')],
    [KeyboardButton(text='Любой другой день')],
    [KeyboardButton(text='Загрузить фото')]
    ]


admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=r_kb_b)
