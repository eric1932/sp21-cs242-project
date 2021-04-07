from time import sleep

from selenium.webdriver.common.keys import Keys

from checkin_template import CheckinTemplate


class Workflow(CheckinTemplate):
    def __init__(self):
        super().__init__("Google Weather")

    def exec(self):
        driver = self._get_driver(headless=False)
        driver.get("https://google.com")
        input_box = driver.find_elements_by_tag_name("input")[0]
        input_box.send_keys("weather in champaign il")
        input_box.send_keys(Keys.RETURN)

        sleep(5)

        driver.quit()
