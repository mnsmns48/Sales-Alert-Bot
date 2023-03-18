from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from handlers.admin import dp


async def cmd_start(m: Message):

    await m.answer_photo(photo='AgACAgIAAxkBAAIFuWQVrxkxJMuUdAUGfGAuXSt448I1AAKgxjEbYxGxSFOciZYzLCoJAQADAgADeQADLwQ',
                         caption='Бот находится в режиме разработки\n'
                                 'Скоро всё будет')


def register_handlers_user():
    dp.register_message_handler(cmd_start, CommandStart())
