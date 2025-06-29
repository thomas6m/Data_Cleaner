# data_cleaner/logger_setup.py

import logging
import coloredlogs
import sys
from data_cleaner.config import DEFAULT_LOG_LEVEL, LOG_FORMAT

def setup_logging(level: int = DEFAULT_LOG_LEVEL) -> logging.Logger:
    """
    Configure and return a logger for the 'data_cleaner' module with colored output.

    Args:
        level (int): Logging level (default: DEFAULT_LOG_LEVEL from config)

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("data_cleaner")

    # Clear existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set log level
    logger.setLevel(level)

    # Setup coloredlogs (adds its own handler)
    coloredlogs.install(
        level=level,
        logger=logger,
        fmt=LOG_FORMAT,
        stream=sys.stdout
    )

    return logger
