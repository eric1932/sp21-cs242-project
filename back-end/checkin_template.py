"""
The template class that will be used to construct checkin tasks
"""
import abc
from typing import Union

from selenium import webdriver


class CheckinTemplate:
    """
    The template class that will be used to construct checkin tasks
    """
    def __init__(self, module_name, use_chromedriver: bool = True):
        self.module_name = module_name
        self.use_chromedriver = use_chromedriver

    # notTODO make private
    def get_driver(self, headless: bool = True) -> Union[webdriver.Chrome, webdriver.Firefox]:
        """
        Get selenium driver
        :param headless: run in background. Required by headless machine. Default: True
        :return: webdriver
        """
        if self.use_chromedriver:
            options = webdriver.ChromeOptions()
            options.headless = headless
            return webdriver.Chrome(options=options)
        else:
            # use GeckoDriver
            # notTODO
            return webdriver.Firefox()

    @abc.abstractmethod
    def exec(self):
        """
        Do whatever needs in order to checkin
        :return: any helpful value
        """
