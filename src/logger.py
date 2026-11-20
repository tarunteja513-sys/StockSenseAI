
import logging
import os
from config import LOG_DIR

# Create log directory
os.makedirs(LOG_DIR, exist_ok=True)

# Log file location
LOG_FILE = os.path.join(LOG_DIR, "stocksense.log")

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# Logger instance
logger = logging.getLogger("StockSenseAI")


def log_info(message):
    logger.info(message)


def log_warning(message):
    logger.warning(message)


def log_error(message):
    logger.error(message)


def log_critical(message):
    logger.critical(message)
