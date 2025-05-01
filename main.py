
import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from logging_config import setup_logger
from core.config import settings
from app.utils.parcer import Parcer
from config import CHAT_ID, NFT_LINKS

from aiolimiter import AsyncLimiter
logger = setup_logger('main')

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

limiter = AsyncLimiter(2, 7)


async def handle_parsing(start_index: int, thread_id: int, url: str):
    """Обработчик одной задачи парсинга с устойчивой отправкой сообщений."""
    async with Parcer() as parcer:
        retry_count = 0
        base_delay = 1  # начальная задержка в секундах
        max_delay = 300  # максимальная задержка (5 минут)

        while True:
            try:
                # Получаем данные для отправки
                answer = await parcer.fetch(str(start_index), url)

                if not answer:
                    logger.info(
                        f"Пустой ответ, повторная попытка через 200 секунд")
                    await asyncio.sleep(200)
                    continue

                # Бесконечные попытки отправки с экспоненциальной задержкой
                send_retry_count = 0
                while True:
                    try:
                        async with limiter:
                            await bot.send_message(
                                CHAT_ID,
                                answer,
                                parse_mode='Markdown',
                                message_thread_id=thread_id
                            )
                            start_index += 1
                            retry_count = 0  # Сбрасываем счетчик ошибок после успеха
                            break  # Выходим из цикла отправки

                    except Exception as send_error:
                        send_retry_count += 1
                        delay = min(
                            base_delay * (2 ** (send_retry_count - 1)), max_delay)
                        logger.error(
                            f"Ошибка отправки в потоке {thread_id} (попытка {send_retry_count}): {send_error}. "
                            f"Повтор через {delay} сек."
                        )
                        await asyncio.sleep(delay)

            except Exception as e:
                retry_count += 1
                delay = min(base_delay * (2 ** (retry_count - 1)), max_delay)
                logger.error(
                    f"Ошибка в потоке {thread_id} ({url}), попытка {retry_count}: {e}. "
                    f"Повтор через {delay} сек."
                )
                await asyncio.sleep(delay)


async def delayed_handle_parsing(delay: float, *args):
    await asyncio.sleep(delay)
    await handle_parsing(*args)


async def on_startup():
    """Функция, которая выполняется при запуске бота."""
    logging.info("Бот запущен.")
    tasks = []

    delay_between_tasks = 0.5  # Задержка в секундах между запусками

    for index, (key, value) in enumerate(NFT_LINKS.items()):
        delay = index * delay_between_tasks
        tasks.append(delayed_handle_parsing(delay, value[1], key, value[0], ))

    await asyncio.gather(*tasks)  # Асинхронно запускаем все задачи

    # async with Parcer() as parcer:
    #     for i in range(0, 10):
    #         while True:
    #             answer = await parcer.fetch(str(i))
    #             if answer:
    #                 await bot.send_message(
    #                     CHAT_ID, answer, parse_mode='Markdown',
    #                     message_thread_id=45
    #                 )
    #                 break
    #             await asyncio.sleep(2)  # подождать перед новой попыткой

    #         await asyncio.sleep(5)  # пауза между задачами
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
