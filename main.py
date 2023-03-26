import asyncio
import logging
import time

from bot import dp
from filter import AdminFilter
from handlers.admin import register_admin_handlers
from handlers.user import register_user_handlers


async def main():
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s', )
    dp.filters_factory.bind(AdminFilter)
    register_admin_handlers()
    register_user_handlers()
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
