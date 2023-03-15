from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboard import admin_kb, data_inline_kb
from db_requests import sales, cur_1, daily_total
from date import date_today, month_today, date_yesterday, month_yesterday

from config import load_config

config = load_config('../.env')

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


async def send_data(call: CallbackQuery):
    if call.data == 'today':
        line = sales(cur_1, date_today, month_today) + daily_total(cur_1, date_today, month_today)
        await call.message.answer(line)
    if call.data == 'yestarday':
        line = sales(cur_1, date_yesterday, month_yesterday) + daily_total(cur_1, date_yesterday, month_yesterday)
        await call.message.answer(line)
    if call.data == 'other':
        await call.message.answer('Введите дату')
        await Wait.text.set()


async def answer_data(m: Message):
    line = sales(cur_1, m.text[0:2], m.text[2:]) + daily_total(cur_1, m.text[0:2], m.text[2:])
    await m.answer(line)


def register_handlers_admin():
    dp.register_message_handler(cmd_start, CommandStart(), state='*', is_admin=True)
    dp.register_message_handler(cmd_start, Text(equals="Начало работы бота", ignore_case=True), state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_callback_query_handler(send_data, state=None)
    dp.register_message_handler(answer_data, state=Wait.text)
