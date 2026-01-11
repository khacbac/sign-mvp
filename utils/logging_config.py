"""
Centralized logging configuration for the sign_mvp project.

Provides consistent logging setup across all modules.
"""

import logging
import sys


def get_logger(name):
    """
    Get a configured logger for a module.

    Args:
        name (str): Logger name (typically __name__ from calling module)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
