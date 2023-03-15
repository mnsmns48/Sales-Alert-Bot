from typing import Optional
from aiogram.dispatcher.filters import BoundFilter
from config import load_config

config = load_config('.env')


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False

        return (obj.from_user.id in config.tg_bot.admin_id) == self.is_admin
