import logging
from logging.handlers import RotatingFileHandler


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Возвращает настроенный логгер.
    Можно использовать в любом модуле проекта.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(
            logging.INFO
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        file_handler = RotatingFileHandler(
            "apps.log", maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
