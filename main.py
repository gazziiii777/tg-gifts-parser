
import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from logging_config import setup_logger
from core.config import settings
from app.utils.parcer import AsyncFetcher
logger = setup_logger('main')

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def on_startup():
    """Функция, которая выполняется при запуске бота."""
    logging.info("Бот запущен.")

    async with AsyncFetcher() as a:
        for i in range(1, 10):
            answer = await a.fetch(str(i))
            if answer:
                await bot.send_message(
                    -1002542039261, answer, parse_mode='Markdown',
                    message_thread_id=2
                )
            await asyncio.sleep(5)
    # Инициализация и подключение к базе данных
    # db_manager = DatabaseManager(DB_PATH)
    # db_manager.connect()

    # Создание таблиц, если они не существуют
    # for table_name, columns in TABLES.items():
    #     db_manager.create_table(table_name, columns)

    # db_manager.close()
    # asyncio.create_task(scheduler())  # Запуск планировщика задач


async def on_shutdown():
    """Функция, которая выполняется при остановке бота."""
    logging.info("Бот остановлен.")
    await bot.close()


async def main():
    """Основная функция, которая запускает бота и планировщик."""
    await on_startup()  # Выполняем startup-логику
    await dp.start_polling(bot)  # Запускаем бота в режиме long-polling


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен вручную.")
    finally:
        asyncio.run(on_shutdown())  # Выполняем shutdown-логику
