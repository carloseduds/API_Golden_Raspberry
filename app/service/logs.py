import logging
from functools import wraps


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app/logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Iniciando execução: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Finalizando execução: {func.__name__}")
        return result
    return wrapper
