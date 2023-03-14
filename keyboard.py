from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date


date_now = date.today()

r_kb_b = [[KeyboardButton(text="Отмена")]]
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=r_kb_b)

data_inline_kb = InlineKeyboardMarkup(row_width=3)
data_inline_kb.add(InlineKeyboardButton(text='Сегодня', callback_data='today'))
