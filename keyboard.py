from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

r_kb_b = [
    [KeyboardButton(text='Начало работы бота')],
    [KeyboardButton(text='Загрузить фото')],
    [KeyboardButton(text='Отмена')]]
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=r_kb_b)

i_btn = [
    InlineKeyboardButton(text='Сегодня', callback_data='today'),
    InlineKeyboardButton(text='Вчера', callback_data='yestarday')
]
data_inline_kb = InlineKeyboardMarkup(row_width=3)
data_inline_kb.add(*i_btn)
data_inline_kb.add(InlineKeyboardButton(text='Другой день', callback_data='other'))

