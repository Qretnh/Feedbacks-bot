import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config.config import get_settings
from app.handlers import include_all_routers
from app.middlewares.i18n import TranslatorRunnerMiddleware
from app.middlewares.session import DbSessionMiddleware
from app.utils.i18n import create_translator_hub


async def main():
    settings = get_settings()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=settings.BOT_TOKEN)

    commands = [BotCommand(command="start", description="🏠 Главное меню")]
    await bot.set_my_commands(commands)
    dp = Dispatcher()
    include_all_routers(dp)

    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.update.middleware(DbSessionMiddleware(Sessionmaker))

    translator_hub: TranslatorHub = create_translator_hub()

    await dp.start_polling(bot, _translator_hub=translator_hub, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
