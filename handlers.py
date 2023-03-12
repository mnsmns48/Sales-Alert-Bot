from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import CommandStart

import fdb

from config import load_config
from keyboard import admin_kb

config = load_config('.env')

bot = Bot(token=config.tg_bot.bot_token)
dp = Dispatcher(bot)

con = fdb.connect(dsn='C:/ClientShopDatabase/TASK2.fdb', user='SYSDBA', password='masterkey')
cur_1 = con.cursor()


def sales(cur, date, month):
    cur.execute(
        f"SELECT CODE, DOC_DATE  FROM DOC_SALE ds WHERE DOC_DATE LIKE '2023-0{month}-0{date} %' ORDER BY DOC_DATE")
    return cur.fetchall()


async def cmd_start(m: types.Message):
    await m.answer("Включен!")


async def show(m: types.Message):
    await m.answer("Введи дату в формате <хх хх>\n"
                       "<день месяц>")


async def date_month(m: types.Message):
    answer_data = m.text
    if answer_data == "Привет":
        await m.answer(f"Вы прислали такую дату: {answer_data}", reply_markup=admin_kb)


def register_all_handlers():
    dp.register_message_handler(date_month)
    dp.register_message_handler(cmd_start, CommandStart())
    dp.register_message_handler(show, commands=['show'])
