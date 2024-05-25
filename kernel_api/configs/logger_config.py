import sys
import logging

from .config import CONFIG

logger = logging.getLogger(
    'KERNEL_API'
)

logger.setLevel(
    level=CONFIG.LOG_LEVEL
)

logger_formatter = logging.Formatter(
    '[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s'
)

logger_handler = logging.StreamHandler(
    sys.stdout
)

logger_handler.setFormatter(
    logger_formatter
)

for existing_handler in logger.handlers:
    logger.removeHandler(
        existing_handler
    )

logger.addHandler(
    logger_handler
)

logger.info(f"The logger has been registered.")
