from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message

from db_requests import goods_list, cur_1
from handlers.admin import dp
from keyboard import user_kb, user_catalog


async def cmd_start(m: Message):
    await m.answer_photo(photo='AgACAgIAAxkBAAIFuWQVrxkxJMuUdAUGfGAuXSt448I1AAKgxjEbYxGxSFOciZYzLCoJAQADAgADeQADLwQ',
                         caption='Бот находится в режиме разработки\n'
                                 'Скоро всё будет', reply_markup=user_kb)


async def catalog(m: Message):
    await m.answer(text='Выбери группу товаров', reply_markup=user_catalog)


async def smart_goods(m: Message):
    await m.answer(text=goods_list(cur_1, 80, 84))


def register_handlers_user():
    dp.register_message_handler(cmd_start, CommandStart())
    dp.register_message_handler(catalog, Text(equals="Каталог товаров", ignore_case=True), state="*")
    dp.register_message_handler(smart_goods, Text(equals="Смартфоны", ignore_case=True), state="*")
