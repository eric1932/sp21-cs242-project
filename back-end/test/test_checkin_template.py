import unittest

from selenium import webdriver

from checkin_template import CheckinTemplate


class MyTestCase(unittest.TestCase):
    def test_get_driver(self):
        driver = CheckinTemplate("test").get_driver(headless=True)
        self.assertIsInstance(driver, webdriver.Chrome)
        driver.quit()


if __name__ == '__main__':
    unittest.main()
