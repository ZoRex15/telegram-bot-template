import asyncio

from dishka import make_async_container

from aiogram import Bot, Dispatcher

from app.infrastructure.di import get_bot_providers
from app.infrastructure.config import DebugConfig
from app.common.logging import setup_logging


async def main():
    dishka = make_async_container(*get_bot_providers())
    debug_config = await dishka.get(DebugConfig)
    setup_logging(debug_config.log_level, debug_config.json_logs)
    bot: Bot = await dishka.get(Bot)
    dp: Dispatcher = await dishka.get(Dispatcher)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dishka.close()

if __name__ == "__main__":
    asyncio.run(main())