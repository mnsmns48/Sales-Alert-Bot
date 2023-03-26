from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot import dp, bot
from firebird_requests import goods_list, cursor
from keyboards.user_kb import user_1_kb, catalog_full_kb, catalog_brand_phones_kb, redmi_inline_kb, realme_inline_kb, \
    samsung_inline_kb, tecno_inline_kb, tcl_inline_kb, media_pad_kb, key_old_phones_kb, watches_kb, catalog_order_kb

from sqlite_requests import read_product, take_caption
from Shippers.process import excel_order_list, xiaomi_del_list, samsung_del_list, text_file_order_list

from config import load_config

config = load_config('../.env')


async def cmd_start(m: Message):
    guest_name = m.from_user.first_name
    await m.answer_photo(photo='AgACAgIAAxkBAAIFuWQVrxkxJMuUdAUGfGAuXSt448I1AAKgxjEbYxGxSFOciZYzLCoJAQADAgADeQADLwQ',
                         caption=f'Привет, {guest_name}, этот Бот находится в режиме тестирования',
                         reply_markup=user_1_kb)


async def catalog(m: Message):
    await m.answer(text='Выбери группу товаров', reply_markup=catalog_full_kb)


async def catalog_phones(m: Message):
    await m.answer(text='Смартфоны', reply_markup=catalog_brand_phones_kb)


async def redmi_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=redmi_inline_kb)


async def realme_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=realme_inline_kb)


async def samsung_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=samsung_inline_kb)


async def tecno_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=tecno_inline_kb)


async def tcl_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=tcl_inline_kb)


async def catalog_media_pad(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=media_pad_kb)


async def catalog_old_key_phones(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=key_old_phones_kb)


async def smart_watches(m: Message):
    await m.answer(text='↓ ↓ ↓ В Наличии', reply_markup=watches_kb)


async def items_order(m: Message):
    await m.answer(text='Товары под заказ доставляются\nот 2-ух до 7-ми дней', reply_markup=catalog_order_kb)


async def apple_order(m: Message):
    text = list()
    result = text_file_order_list('Shippers/apple.txt')
    for k, v in result.items():
        text.append((str(k) + ' - ' + str(v)))
    line = '↓ ↓ ↓ ↓ В течение 2-7 дней:\n\n' + '\n'.join(text)
    if len(line) > 4096:
        for i in range(0, len(line), 4096):
            part_mess = line[i: i + 4096]
            await m.answer(part_mess)
            time.sleep(1)
    else:
        await m.answer(text=line)
    await m.answer('Обращайтесь @tser88 или @cifrotech_mobile')


async def xiaomi_order(m: Message):
    result = excel_order_list('Shippers/xiaomi.xlsx', xiaomi_del_list)
    mess = '↓ ↓ ↓ ↓ В течение 2-7 дней:\n\n' + ''.join(str(item) + '\n' for item in result)
    if len(mess) > 4096:
        for i in range(0, len(mess), 4096):
            part_mess = mess[i: i + 4096]
            await m.answer(part_mess)
            time.sleep(1)
    else:
        await m.answer(mess)
    await m.answer('Обращайтесь @tser88 или @cifrotech_mobile')


async def samsung_order(m: Message):
    result = excel_order_list('Shippers/samsung.xlsx', samsung_del_list)
    mess = '↓ ↓ ↓ ↓ В течение 2-7 дней:\n\n' + ''.join(str(item) + '\n' for item in result)
    if len(mess) > 4096:
        for i in range(0, len(mess), 4096):
            part_mess = mess[i: i + 4096]
            await m.answer(part_mess)
            time.sleep(1)
    else:
        await m.answer(mess)
    await m.answer('Обращайтесь @tser88 или @cifrotech_mobile')


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
        await bot.send_photo(chat_id=chat_id,
                             photo=read_product(name='PHOTO', code='CODE', product_code=code_product)[0],
                             caption=caption)


async def smart_goods(m: Message):
    txt = list()
    result = goods_list(cursor, 80, 84)
    for row in result:
        txt.append(f'{row[1]}\nЦена: {int(row[3])} руб\n\n')
    line = ''.join(txt)
    txt.clear()
    await m.answer(text=line)


def register_user_handlers():
    dp.register_message_handler(cmd_start, CommandStart())
    dp.register_callback_query_handler(show_product)
    dp.register_message_handler(catalog, text="Товары в наличии")
    dp.register_message_handler(smart_goods, text="Полный список смартфонов")
    dp.register_message_handler(catalog_phones, text="Смартфоны")
    dp.register_message_handler(redmi_phones, text="Xiaomi / Redmi / Poco")
    dp.register_message_handler(realme_phones, text="Realme / Oppo / OnePlus")
    dp.register_message_handler(samsung_phones, text="Samsung")
    dp.register_message_handler(tecno_phones, text="Tecno / Infinix")
    dp.register_message_handler(tcl_phones, text="TCL")
    dp.register_message_handler(cmd_start, text="Перейти в начало")
    dp.register_message_handler(catalog_media_pad, text="Планшеты")
    dp.register_message_handler(catalog_old_key_phones, text="Кнопочные телефоны")
    dp.register_message_handler(smart_watches, text="Умные часы")
    dp.register_message_handler(items_order, text="Под заказ")
    dp.register_message_handler(apple_order, text="Apple под заказ")
    dp.register_message_handler(xiaomi_order, text="Xiaomi под заказ")
    dp.register_message_handler(samsung_order, text='Samsung под заказ')
