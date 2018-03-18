import logging
import os
import datetime
from logging.handlers import TimedRotatingFileHandler


def create_loggers(app):
    log_path = app.config['root_path'] + "/" + app.config['log_path'] + "/"
    ensure_dir(log_path)
    rotation_logger = create_rotating_logger(log_path)

    setattr(app, 'loggers', {
        "rotating": rotation_logger
    })


def create_rotating_logger(path):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.ERROR)
    file_name = "rotating" + datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    handler = TimedRotatingFileHandler(path+file_name,
                                       when="d",
                                       interval=1,
                                       backupCount=5)
    logger.addHandler(handler)
    return logger


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
