from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date, timedelta

from firebird_requests import sales_one_day, cursor
from keyboards.admin_kb import admin_kb
from bot import dp

from config import load_config

config = load_config('../.env')

date_today = date.today()
date_yesterday = date_today - timedelta(days=1)
date_today = str(date_today)
date_yesterday = str(date_yesterday)


class Wait(StatesGroup):
    text = State()
    photo = State()


async def cmd_start(m: Message):
    await m.answer("--Режим админа--", reply_markup=admin_kb)


async def choose_date(m: Message):
    if m.text == 'Сегодня':
        line = sales_one_day(cursor, date=date_today)
        await m.answer(line)
    if m.text == 'Вчера':
        line = sales_one_day(cursor, date=date_yesterday)
        await m.answer(line)
    if m.text == "Любой другой день":
        await m.answer('Введите дату в формате: ХХХХ\nХХ - ДЕНЬ ХХ - МЕСЯЦ\nнапример: 0303\n'
                       'Будет показан отчет\nза 3 марта текущего года\n\n'
                       'Еcли ввести дату в формате: ХХХХХХ\n'
                       'ХХ - ДЕНЬ ХХ - МЕСЯЦ ХХ - ГОД\n'
                       'напрмер: 030320\n'
                       'Будет показан отчет\nза 3 марта 2020 года')
        await Wait.text.set()


async def answer_date_another_day(m: Message, state: FSMContext):
    if m.text.isdigit():
        if len(m.text) == 4:
            date_r = '2023' + '-' + str(m.text[2:]) + '-' + m.text[:2]
        if len(m.text) == 6:
            date_r = '20' + str(m.text[4:]) + '-' + str(m.text[2:4]) + '-' + str(m.text[0:2])
        line = sales_one_day(cursor, date=date_r)
        await m.answer(line)
        await state.finish()
    else:
        await m.answer('Введите дату в нужном формате!\n\n'
                       'Читай инструкцию сверху')
        await state.finish()


async def push_load_photo(m: Message):
    await m.answer('Добавь фото')
    await Wait.photo.set()


async def load_get_photo_id(m: Message, state=FSMContext):
    id_photo = m.photo[-1].file_id
    await m.answer('ID на сервере Telegram:')
    await m.answer(id_photo)
    await state.finish()


def register_admin_handlers():
    dp.register_message_handler(cmd_start, CommandStart(), is_admin=True)
    dp.register_message_handler(choose_date, text=["Сегодня",
                                                   "Вчера",
                                                   "Любой другой день", ])
    dp.register_message_handler(answer_date_another_day, state=Wait.text)
    dp.register_message_handler(push_load_photo, text="Загрузить фото")
    dp.register_message_handler(load_get_photo_id, content_types=['photo'], state=Wait.photo)
