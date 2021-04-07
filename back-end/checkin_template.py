import abc
from typing import Union

from selenium import webdriver


class CheckinTemplate:
    def __init__(self, module_name, use_chromedriver: bool = True):
        self.module_name = module_name
        self.use_chromedriver = use_chromedriver

    def _get_driver(self, headless: bool = True) -> Union[webdriver.Chrome, webdriver.Firefox]:
        if self.use_chromedriver:
            options = webdriver.ChromeOptions()
            options.headless = headless
            return webdriver.Chrome(options=options)
        else:
            # use GeckoDriver
            pass

    @abc.abstractmethod
    def exec(self):
        pass
