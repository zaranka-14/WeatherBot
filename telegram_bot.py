import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from config_reader import config
import common


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    storage = RedisStorage.from_url("redis://redis:6379/3")

    dp = Dispatcher(storage=storage)
    bot = Bot(config.bot_token.get_secret_value())

    dp.include_router(common.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
