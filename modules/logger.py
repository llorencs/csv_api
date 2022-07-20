"""
Logger module
"""

import logging
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = TimedRotatingFileHandler('csv_tools.log', encoding='utf-8', when='D', interval=30, backupCount=10)
format_log = logging.Formatter('%(asctime)s - %(levelname)s: %(filename)s - %(lineno)d - %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p')
file_handler.setFormatter(format_log)
console_handler = logging.StreamHandler()
console_handler.setFormatter(format_log)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
