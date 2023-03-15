import asyncio
import logging

from filter import AdminFilter
from handlers.admin import dp, register_handlers_admin
from handlers.user import register_handlers_user


async def main():
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s', )
    dp.filters_factory.bind(AdminFilter)
    register_handlers_admin()
    register_handlers_user()
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
