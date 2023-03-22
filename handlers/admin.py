from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from firebird_requests import sales, cursor, daily_total
from date import date_today, month_today, date_yesterday, month_yesterday
from keyboards.admin_kb import admin_kb, data_inline_kb
from bot import dp

from config import load_config

config = load_config('../.env')


class Wait(StatesGroup):
    text = State()
    photo = State()


async def cmd_start(m: Message):
    await m.answer("--Режим админа--", reply_markup=admin_kb)
    await m.answer("Показать продажи за:", reply_markup=data_inline_kb)


@dp.callback_query_handler()
async def send_data(call: CallbackQuery):
    if call.data == 'today':
        line = sales(cursor, date_today, month_today) + daily_total(cursor, date_today, month_today)
        await call.message.answer(line)
    if call.data == 'yesterday':
        line = sales(cursor, date_yesterday, month_yesterday) + daily_total(cursor, date_yesterday, month_yesterday)
        await call.message.answer(line)
    if call.data == 'other':
        await call.message.answer('Введите дату')
        await Wait.text.set()


@dp.message_handler(content_types=['photo'], state="*")
async def load_get_photo_id(m: Message):
    await m.answer('добавь фото')
    await Wait.photo.set()
    id_photo = m.photo[-1].file_id
    await m.answer('ID на сервере Telegram:')
    await m.answer(id_photo)


async def answer_data(m: Message):
    line = sales(cursor, m.text[0:2], m.text[2:]) + daily_total(cursor, m.text[0:2], m.text[2:])
    await m.answer(line)


async def cmd_cancel(m: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await m.answer("Отмена\nДля начала работы на пиши /start", reply_markup=ReplyKeyboardRemove())


def register_handlers_admin():
    dp.register_message_handler(cmd_start, CommandStart(), state="*", is_admin=True)
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена", ignore_case=True), state="*", is_admin=True)
    dp.register_message_handler(answer_data, state=Wait.text, is_admin=True)
