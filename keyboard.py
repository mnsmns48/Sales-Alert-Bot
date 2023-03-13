from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import date
from dicts import days, month

date_now = date.today()

kb_b = [
    [KeyboardButton(text="Отмена", callback_data='cancel')],
    [],
    [KeyboardButton(text="Сегодня", callback_data='today')]
]

for i in range(3, 0, -1):
    for k, v in days[date_now.weekday() - i].items():
        kb_b[1].append(KeyboardButton(text=f"{date_now.day - i} "
                                           f"{month[date_now.month - 1].get(date_now.month)}\n"
                                           f"{v}",
                                      callback_data=f"{date_now.day - i}"))

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=kb_b)
