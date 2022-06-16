import sys
import logging
from logging.handlers import TimedRotatingFileHandler


class Logger:

    def __init__(self, 
                log_file='etl.log', 
                log_format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s"):

        self.log_file = log_file
        self.formatter = logging.Formatter(log_format)
        
    def get(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.__get_file_handler__())
        logger.addHandler(self.__get_console_handler__())
        logger.propagate = False
        return logger

    def __get_console_handler__(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def __get_file_handler__(self):
        file_handler = TimedRotatingFileHandler(self.log_file, when='midnight')
        file_handler.setFormatter(self.formatter)
        return file_handler


def get(logger_name):
    return Logger().get(logger_name)