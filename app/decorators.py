import logging
from functools import wraps

from .log import logger


def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Iniciando execução: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Finalizando execução: {func.__name__}")
        return result
    return wrapper
