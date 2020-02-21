import logging
import os


filename = 'juicer'

logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler(f'{filename}.log')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

def increase_log_level():
    levels = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG'
    }
    current = rootLogger.level
    logging.debug(f'Current log level: {levels.get(current)} ({current})')
    if current > 10:
        new_level = current - 10
        if new_level % 10 == 0 and new_level in range(10,51):
            logging.debug(f'Setting log level to {levels.get(new_level)} ({new_level})')
            rootLogger.setLevel(current - 10)
            logging.debug(f'Set log level to {levels.get(new_level)} ({new_level})')