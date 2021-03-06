"""
Get today's google logo & check the weather in Champaign.
"""
from time import sleep

from selenium.webdriver.common.keys import Keys

from checkin_misc.checkin_class_template import CheckinTemplate, log


class Workflow(CheckinTemplate):
    """
    The workflow for this task
    """
    def __init__(self, *args, **kwargs):
        super().__init__("Google Weather", *args, **kwargs)

    @log
    def exec(self):
        driver = self.get_driver(headless=False)
        driver.get("https://google.com")

        image = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/img")
        image_url = image.get_attribute("src")

        input_box = driver.find_element_by_tag_name("input")
        input_box.send_keys("weather in champaign il")
        input_box.send_keys(Keys.RETURN)

        sleep(5)

        driver.quit()  # notTODO func modifier

        return image_url


if __name__ == '__main__':
    Workflow().exec()
