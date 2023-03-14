import logging
from aiogram import executor
from handlers import dp, register_all_handlers
from config import load_config


config = load_config('.env')
logging.basicConfig(level=logging.INFO,
                    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s', )

if __name__ == '__main__':
    register_all_handlers()
    executor.start_polling(dp, skip_updates=True)
