# logger_config.py
import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name):
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Минимальный уровень логирования

    # Формат сообщений
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Обработчик для записи в файл
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=1024*1024*100,  # 1 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger