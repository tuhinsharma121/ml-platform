import logging
import logging.config
import os

from config import *


def configure_logger(name, log_path):
    """Configures the logger

    Parameters
    ----------
    name : str
        Name of the python logger
    log_path : str
        Filepath for storing the log. Make sure write permission is enabled for the path

    Returns
    -------
    logger :

    """
    directory = os.path.dirname(log_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    logging.config.dictConfig({
        "version": 1,
        "formatters": {
            "kronos_logger": {
                "class": "logging.Formatter",
                "format": "%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "level": LOGGING_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "kronos_logger",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "level": LOGGING_LEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "kronos_logger",
                "filename": log_path
            }
        },
        "loggers": {
            "kronos_logger": {
                "level": LOGGING_LEVEL,
                "handlers": ["console", "file"]
            }
        },
    })
    logger = logging.getLogger(name)
    logger.propagate = False

    return logger
