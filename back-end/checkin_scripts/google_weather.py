from time import sleep

from selenium.webdriver.common.keys import Keys

from checkin_template import CheckinTemplate


class Workflow(CheckinTemplate):
    def __init__(self):
        super().__init__("Google Weather")

    def exec(self):
        driver = self._get_driver(headless=False)
        driver.get("https://google.com")

        image = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/img")
        image_url = image.get_attribute("src")

        input_box = driver.find_element_by_tag_name("input")
        input_box.send_keys("weather in champaign il")
        input_box.send_keys(Keys.RETURN)

        sleep(5)

        driver.quit()  # TODO func modifier

        return image_url
