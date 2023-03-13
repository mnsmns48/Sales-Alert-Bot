from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import CommandStart

import fdb

from config import load_config
from keyboard import admin_kb, date_now

config = load_config('.env')

bot = Bot(token=config.tg_bot.bot_token)
dp = Dispatcher(bot)

con = fdb.connect(dsn='C:/Users/DrKoffer/PycharmProjects/Sales-Alert-Bot/TASK2.fdb', user='SYSDBA',
                  password='masterkey')
cur_1 = con.cursor()


def sales(cur, date, month):
    cur.execute(
        f"SELECT ds.DOC_DATE, dg.NAME, dst.QUANTITY, dst.PRICE2, dst.SUMMA2, ds.NONCASH "
        f"FROM DOC_SALE ds, DOC_SALE_TABLE dst , DIR_GOODS dg "
        f"WHERE ds.DOC_DATE LIKE '2023-0{month}-{date}%' AND ds.CODE = dst.CODE AND dst.GOOD = dg.CODE "
        f"ORDER BY DOC_DATE")
    return cur.fetchall()


async def cmd_start(m: types.Message):
    await m.answer("Покажу отчет о продажах", reply_markup=admin_kb)


async def send_today(call: types.CallbackQuery):
    for i in sales(cur_1, 12, 3):
        await call.message.answer(str(i[0])[11:16], i[1], int(i[2]), int(i[3]), int(i[4]),
                                  "" if int(i[5]) == 0 else "Безнал")


def register_all_handlers():
    dp.register_callback_query_handler(text='today')
    dp.register_message_handler(cmd_start, CommandStart())
