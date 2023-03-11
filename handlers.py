from aiogram import Dispatcher, Bot, types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import load_config

config = load_config('.env')

bot = Bot(token=config.tg_bot.bot_token)
dp = Dispatcher(bot)


async def setup_commands(dp: Dispatcher):
    bot_commands = [
        BotCommand(command='/start', description="Начало работы"),
        BotCommand(command='/test', description="На данный момент не работает")
    ]
    await dp.bot.set_my_commands(bot_commands)
    await


async def cmd_start(m: types.Message):
    # kb = [
    #     [types.KeyboardButton(text="Test")],
    #     [types.KeyboardButton(text="Test_1")]
    # ]
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await m.answer("Включен!")


def register_all_handlers():
    dp.register_message_handler(cmd_start, CommandStart())
