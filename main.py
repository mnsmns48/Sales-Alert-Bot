import asyncio
import logging

from bot import dp
from filter import AdminFilter
from handlers.admin import register_handlers_admin



async def main():
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s', )
    dp.filters_factory.bind(AdminFilter)
    register_handlers_admin()
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
