import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from .di import di_container
from .view import handlers

redis = Redis(
    host='localhost',
    port=6379,
    db=1
)
dispatcher = Dispatcher(
    storage=RedisStorage(redis=redis)
)
dispatcher.include_router(handlers.router)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=('%(asctime)s - [%(levelname)s] - %(name)s - '
                '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'),
        handlers=[
            logging.FileHandler('logs.log'),
            logging.StreamHandler()
        ]

    )

    bot = Bot(
        token=di_container.settings.auth_token
    )

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
