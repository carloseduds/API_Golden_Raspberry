import logging

# Configurar o logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app/logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
