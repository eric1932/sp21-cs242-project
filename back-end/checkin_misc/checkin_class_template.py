"""
The template class that will be used to construct checkin tasks
"""
import abc
from typing import Union

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from checkin_misc.task_logging import get_module_logger


def log(func):
    def wrapper(self, *args, **kwargs):
        ret_val = func(self, *args, **kwargs)
        self.logger.info(ret_val)
        return ret_val

    return wrapper


class CheckinTemplate:
    """
    The template class that will be used to construct checkin tasks
    """
    def __init__(self, module_name, use_chromedriver: bool = True):
        self.module_name = module_name
        self.use_chromedriver = use_chromedriver
        self.logger = get_module_logger(module_name)

    # notTODO make private
    def get_driver(self, headless: bool = True, eager: bool = False) -> Union[webdriver.Chrome, webdriver.Firefox]:
        """
        Get selenium driver
        :param headless: run in background. Required by headless machine. Default: True
        :param eager: load page eagerly (ref: https://stackoverflow.com/a/46339092/8448191)
        :return: webdriver
        """
        if self.use_chromedriver:
            options = webdriver.ChromeOptions()
            options.headless = headless

            caps = DesiredCapabilities().CHROME
            if eager:
                caps["pageLoadStrategy"] = "eager"

            return webdriver.Chrome(
                options=options,
                desired_capabilities=caps
            )
        else:
            # use GeckoDriver
            # notTODO
            caps = DesiredCapabilities().FIREFOX
            if eager:
                caps["pageLoadStrategy"] = "eager"

            return webdriver.Firefox()

    @abc.abstractmethod
    def exec(self):
        """
        Do whatever needs in order to checkin
        :return: any helpful value
        """
