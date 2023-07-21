import os
import sys
import logging
from functools import wraps

def logger_class(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'self' in kwargs:
            # Logging for class methods
            cls = kwargs['self'].__class__.__name__
            logger = logging.getLogger(f"{cls}.{func.__name__}")
        else:
            # Logging for regular functions
            logger = logging.getLogger(func.__module__)

        logger.setLevel(logging.INFO)

        # Add a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Add a file handler
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, "app.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        try:
            logger.info(f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} execution successful. Result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error occurred while executing {func.__name__}: {e}")
            raise

    return wrapper
