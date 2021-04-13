import logging
import os
import sys

LOG_PATH = "logs"
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

logger_dict = {}


def get_module_logger(module_name: str):
    # ref: https://www.cnblogs.com/first-semon/p/8588285.html
    if module_name in logger_dict:
        return logger_dict[module_name][0]
    else:
        _logger = logging.getLogger(module_name)
        print(os.getcwd())  # TODO
        file_handler = logging.FileHandler(os.path.join("..", LOG_PATH, module_name) + ".log")
        console_handler = logging.StreamHandler(sys.stdout)
        _logger.addHandler(file_handler)
        _logger.addHandler(console_handler)

        logger_dict[module_name] = (_logger, file_handler, console_handler)

        return _logger


if __name__ == '__main__':
    logger = get_module_logger("test")
    logger.warning("Hello!")
