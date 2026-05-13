import asyncio

from aiogram import Bot, Dispatcher

from src.config import settings
from src.handlers import build_router
from src.service import BotService
from src.storage import JsonStorage


async def _main() -> None:
    bot = Bot(token=settings.tg_token)
    dispatcher = Dispatcher()
    storage = JsonStorage(
        email_store_path=settings.email_store_path,
        taken_email_store_path=settings.taken_email_store_path,
        user_locale_store_path=settings.user_locale_store_path,
    )
    service = BotService(settings=settings, storage=storage)

    dispatcher.include_router(build_router(service))

    try:
        await dispatcher.start_polling(bot)
    finally:
        await service.shutdown()
        await bot.session.close()


def run() -> None:
    asyncio.run(_main())
