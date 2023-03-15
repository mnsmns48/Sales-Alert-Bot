from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    dsn: str
    user: str
    password: str


@dataclass
class TgBot:
    bot_token: str
    admin_id: list[int]


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str = None):
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            bot_token=env.str("BOT_TOKEN"),
            admin_id=list(map(int, env.list("ADMIN_ID"))),
        ),
        db=DbConfig(
            dsn=env.str('DB_DSN'),
            user=env.str('DB_USER'),
            password=env.str('DB_PASSWORD'),
        ),
    )
