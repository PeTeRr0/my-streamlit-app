# utils/helpers.py

import logging
import sys
from datetime import datetime

def setup_logger(name=__name__, level=logging.INFO):
    """
    Create and return a logger with specified name and level.
    Logs will stream to stdout by default.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # If the logger has no handlers, add one
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

def format_date(date_str, date_format="%Y-%m-%d"):
    """
    Convert a string date into a datetime object with a given format.
    Returns None if parsing fails.
    """
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        return None

def handle_api_error(response):
    """
    Check the status code of a requests response.
    Logs error & raises an exception if non-200 status code.
    """
    if response.status_code != 200:
        logging.error(f"API returned status code: {response.status_code}")
        logging.error(f"Response content: {response.text}")
        raise Exception("API Error")
    return response

# Additional helpers can be added as needed...
