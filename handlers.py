from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboard import admin_kb, data_inline_kb
from db_requests import sales, cur_1
from date import date_today, month_today, date_yesterday, month_yesterday

from config import load_config

config = load_config('.env')

bot = Bot(token=config.tg_bot.bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class Wait(StatesGroup):
    text = State()


async def cmd_start(m: Message, state: FSMContext):
    await state.finish()
    await m.answer("--Режим админа--", reply_markup=admin_kb)
    await m.answer("Показать продажи за:", reply_markup=data_inline_kb)


async def cmd_cancel(m: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await m.answer("Отмена\nДля начала работы на пиши /start", reply_markup=ReplyKeyboardRemove())


async def send_data(call: CallbackQuery, state: FSMContext):
    if call.data == 'today':
        line = 'Сегодня'
        # data = sales(cur_1, date_today, month_today)
    if call.data == 'yestarday':
        line = 'Вчера'
        # data = sales(cur_1, date_yesterday, month_yesterday)
    if call.data == 'other':
        await call.message.answer("Дата в формате ХХ ХХ")
        await Wait.text.set()
        await call.message.answer(data_text)
        # data_list = []
    # for row in data:
    #     no_cash = '----- Оплата картой\n' if row[5] == 1 else ''
    #     data_list.append(f"{str(row[0])[11:16]} {row[1]}\n--"
    #                      f"{int(row[2])}--{int(row[3])}--итого: <{int(row[4])}>\n{no_cash}\n")
    # line = ''.join(data_list)
    # await call.message.answer(line)


async def req_date(m: Message, state=FSMContext):
    async with state.proxy() as data:
        global data_text
        data_text = m.text




def register_all_handlers():
    dp.register_message_handler(cmd_start, CommandStart(), state='*')
    dp.register_message_handler(cmd_start, Text(equals="Начало работы бота", ignore_case=True), state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_callback_query_handler(send_data)
    dp.register_message_handler(req_date, state=Wait.text)
