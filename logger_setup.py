import logging
import coloredlogs
import sys

def setup_logging(level=logging.INFO):
    """
    Configure and return a logger for the 'data_cleaner' module with colored output.
    
    Args:
        level (int): Logging level (default: logging.INFO)
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("data_cleaner")

    # Clear existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set log level
    logger.setLevel(level)

    # Setup coloredlogs (this adds its own handler)
    coloredlogs.install(
        level=level,
        logger=logger,
        fmt="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout
    )

    return logger
