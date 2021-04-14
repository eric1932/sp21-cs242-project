import unittest

from selenium import webdriver

from checkin_misc.checkin_class_template import CheckinTemplate


class MyTestCase(unittest.TestCase):
    def test_get_driver_chrome(self):
        driver = CheckinTemplate("test").get_driver(eager=True)
        self.assertIsInstance(driver, webdriver.Chrome)
        driver.quit()

    def test_get_driver_firefox(self):
        driver = CheckinTemplate("test", use_chromedriver=False).get_driver(eager=True)
        self.assertIsInstance(driver, webdriver.Firefox)
        driver.quit()


if __name__ == '__main__':
    unittest.main()
