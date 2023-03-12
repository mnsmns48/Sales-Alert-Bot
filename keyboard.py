from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import date
from dicts import days, month

date_now = date.today()

sales_data = ()
db2_yesterday = KeyboardButton(f"{date_now.day - 3} {month.get(date_now.month)}\n"
                               f"{days.get(date_now.weekday() - 2)}")
db1_yesterday = KeyboardButton(f"{date_now.day - 2} {month.get(date_now.month)}\n"
                               f"{days.get(date_now.weekday() - 1)}")
yesterday = KeyboardButton(f"{date_now.day - 1} {month.get(date_now.month)}\n"
                           f"{days.get(date_now.weekday())}")
today = KeyboardButton("Сегодня")
cancel = KeyboardButton("Отмена")

kb_b = [
        [cancel],
        [db2_yesterday, db1_yesterday, yesterday],
        [today]
    ]

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=kb_b)
