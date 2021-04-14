import logging
import os
import sys

ROOT_DIR_NAME = "back-end"
LOG_DIR_NAME = "logs"
FULL_PREFIX = os.getcwd()
while (dir_name := os.path.split(FULL_PREFIX)[1]) and dir_name != ROOT_DIR_NAME:
    FULL_PREFIX = os.path.split(FULL_PREFIX)[0]
FULL_LOG_PATH = os.path.join(FULL_PREFIX, LOG_DIR_NAME)
if not os.path.exists(FULL_LOG_PATH):
    os.mkdir(FULL_LOG_PATH)

logger_dict = {}


def get_module_logger(module_name: str) -> logging.Logger:
    # ref: https://www.cnblogs.com/first-semon/p/8588285.html
    if module_name in logger_dict:
        return logger_dict[module_name][0]
    else:
        _logger = logging.getLogger(module_name)
        _formatter = logging.Formatter('%(asctime)s,%(levelname)-12s:%(message)s')
        file_handler = logging.FileHandler(f"{os.path.join(FULL_LOG_PATH, module_name)}.log")
        file_handler.setFormatter(_formatter)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(_formatter)
        _logger.addHandler(file_handler)
        _logger.addHandler(console_handler)

        _logger.setLevel(logging.INFO)

        logger_dict[module_name] = (_logger, file_handler, console_handler)

        return _logger


if __name__ == '__main__':
    logger = get_module_logger("test")
    logger.warning("Hello!")
