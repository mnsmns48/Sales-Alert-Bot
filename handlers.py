from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import CommandStart
from keyboard import admin_kb, data_inline_kb
from db_requests import sales, cur_1

from config import load_config
config = load_config('.env')

bot = Bot(token=config.tg_bot.bot_token)
dp = Dispatcher(bot)


async def cmd_start(m: types.Message):
    await m.answer("!", reply_markup=admin_kb)
    await m.answer("Отчет за сегодня:", reply_markup=data_inline_kb)


async def send_today(call: types.CallbackQuery):
    data = sales(cur_1, '12', '03')
    data_list = []
    for row in data:
        no_cash = '----- Оплата картой\n' if row[5] == 1 else ''
        data_list.append(f"{str(row[0])[11:16]} {row[1]}\n   К-ВО: "
                         f"{int(row[2])}--{int(row[3])}--ИТОГО: <{int(row[4])}>\n{no_cash}\n")
    line = ''.join(data_list)
    await call.message.answer(line)


def register_all_handlers():
    dp.register_callback_query_handler(send_today, text='today')
    dp.register_message_handler(cmd_start, CommandStart())
