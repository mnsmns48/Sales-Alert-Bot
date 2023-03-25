from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from firebird_requests import goods_list, cursor

samsung_phone_path = 80
realme_phone_path = 81
redmi_phone_path = 82
tecno_phone_path = 83
tcl_phone_path = 84
mediapad_phone_path = 29
key_old_phones = 28

code = 0
name = 1
amount = 2
price = 3


def show(column, path):
    txt = list()
    result = goods_list(cursor, path, path)
    for row in result:
        txt.append(f'{row[column]}')
    line = ''.join(txt)

    return txt


user_1 = [
    [KeyboardButton(text='Каталог товаров')],
    [KeyboardButton(text='Услуги')],
    [KeyboardButton(text='Информация')],
]

catalog_full = [
    [KeyboardButton(text='Смартфоны')],
    [KeyboardButton(text='Планшеты')],
    [KeyboardButton(text='Кнопочные телефоны')],
]

catalog_brand_phones = [
    [KeyboardButton(text='Xiaomi / Redmi / Poco')],
    [KeyboardButton(text='Realme / Oppo / OnePlus')],
    [KeyboardButton(text='Samsung')],
    [KeyboardButton(text='Tecno / Infinix')],
    [KeyboardButton(text='TCL')],
    [KeyboardButton(text='Полный список смартфонов')],
    [KeyboardButton(text='Перейти в начало')]
]

user_1_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=user_1)
catalog_full_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=catalog_full)
catalog_brand_phones_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False,
                                              keyboard=catalog_brand_phones)

redmi_inline_kb = InlineKeyboardMarkup()
for i, c in zip(show(name, redmi_phone_path), show(code, redmi_phone_path)):
    redmi_inline_kb.add(InlineKeyboardButton(text=i[9:], callback_data=c))

realme_inline_kb = InlineKeyboardMarkup()
for i, c in zip(show(name, realme_phone_path), show(code, realme_phone_path)):
    realme_inline_kb.add(InlineKeyboardButton(text=i[9:], callback_data=c))

samsung_inline_kb = InlineKeyboardMarkup()
for i, c in zip(show(name, samsung_phone_path), show(code, samsung_phone_path)):
    samsung_inline_kb.add(InlineKeyboardButton(text=i[9:], callback_data=c))

tecno_inline_kb = InlineKeyboardMarkup()
for i, c in zip(show(name, tecno_phone_path), show(code, tecno_phone_path)):
    tecno_inline_kb.add(InlineKeyboardButton(text=i[9:], callback_data=c))

tcl_inline_kb = InlineKeyboardMarkup()
for i, c in zip(show(name, tcl_phone_path), show(code, tcl_phone_path)):
    tcl_inline_kb.add(InlineKeyboardButton(text=i[9:], callback_data=c))

media_pad_kb = InlineKeyboardMarkup()
for i, c in zip(show(name, mediapad_phone_path), show(code, mediapad_phone_path)):
    media_pad_kb.add(InlineKeyboardButton(text=i[8:], callback_data=c))

key_old_phones_kb = InlineKeyboardMarkup()
for i, c, p in zip(show(name, key_old_phones), show(code, key_old_phones), show(price, key_old_phones)):
    key_old_phones_kb.add(InlineKeyboardButton(
        text=f'{p[:-2]} {i[18:]}', callback_data=c))
