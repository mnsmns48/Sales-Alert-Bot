from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery

from firebird_requests import goods_list, cursor
from bot import dp, bot
from keyboards.user_kb import *
from sqlite_requests import read_product, take_caption
from config import load_config

config = load_config('../.env')


@dp.register_message_handler(CommandStart(), Text(equals="Перейти в начало", ignore_case=True), state="*")
async def cmd_start(m: Message):
    await m.answer_photo(photo='AgACAgIAAxkBAAIFuWQVrxkxJMuUdAUGfGAuXSt448I1AAKgxjEbYxGxSFOciZYzLCoJAQADAgADeQADLwQ',
                         caption='Бот находится в режиме разработки\n'
                                 'Скоро всё будет', reply_markup=user_1_kb)


@dp.message_handler(Text(equals="Каталог товаров", ignore_case=True), state="*")
async def catalog(m: Message):
    await m.answer(text='Выбери группу товаров', reply_markup=catalog_full_kb)


@dp.message_handler(Text(equals="Смартфоны", ignore_case=True), state="*")
async def catalog_phones(m: Message):
    await m.answer(text='Смартфоны', reply_markup=catalog_brand_phones_kb)


@dp.message_handler(Text(equals="Xiaomi / Redmi / Poco", ignore_case=True), state="*")
async def redmi_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=redmi_inline_kb)


@dp.message_handler(Text(equals="Realme / Oppo / OnePlus", ignore_case=True), state="*")
async def realme_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=realme_inline_kb)


@dp.message_handler(Text(equals="Samsung", ignore_case=True), state="*")
async def samsung_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=samsung_inline_kb)


@dp.message_handler(Text(equals="Tecno / Infinix", ignore_case=True), state="*")
async def tecno_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=tecno_inline_kb)


@dp.message_handler(Text(equals="TCL", ignore_case=True), state="*")
async def tecno_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=tcl_inline_kb)


@dp.callback_query_handler()
async def show_product(callback: CallbackQuery):
    code_product = callback.data
    chat_id = callback.from_user.id
    caption = take_caption(code_product)
    pic = read_product(name='PHOTO', code='CODE', product_code=code_product)
    if pic is None or pic[0] is None:
        pic = open(str(config.misc_path.photo + str(code_product) + '.jpg'), 'rb')
        await bot.send_photo(chat_id=chat_id, photo=pic, caption=caption)
        pic.close()
    else:
        await bot.send_photo(chat_id=chat_id, photo=read_product(name='PHOTO', code='CODE', product_code=16416)[0],
                             caption=caption)


@dp.message_handler(Text(equals="Полный список смартфонов", ignore_case=True), state="*")
async def smart_goods(m: Message):
    txt = list()
    result = goods_list(cursor, 80, 84)
    for row in result:
        txt.append(f'{row[1]}\nЦена: {int(row[3])} руб\n\n')
    line = ''.join(txt)
    txt.clear()
    await m.answer(text=line)
