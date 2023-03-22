from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
from config import load_config
config = load_config('../.env')

bot = Bot(token=config.tg_bot.bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())