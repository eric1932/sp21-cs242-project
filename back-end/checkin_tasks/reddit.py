import json
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from checkin_misc.checkin_class_template import CheckinTemplate, log


class Workflow(CheckinTemplate):
    def __init__(self):
        super().__init__("Reddit")

    @log
    def exec(self):
        try:
            driver = self.get_driver(headless=False, eager=True)
            driver.get("https://www.reddit.com")

            with open("r_cookies.json") as f:
                cookies = json.load(f)

            for each_cookie in cookies:
                driver.add_cookie(each_cookie)

            driver.get("https://www.reddit.com/settings")

            # Coin button
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable([By.XPATH,
                                            "/html/body/div[1]/div/div[2]/div[1]/header/div/div[2]/div[2]/div/div[1]"
                                            "/span[4]/button"])) \
                .click()

            # Coin button #2
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[2]/div[1]/div[2]/button"))) \
                .click()

            email = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div"
                                                 "/div[2]/div[1]/div[1]/div[1]/p").text

            # for demo
            time.sleep(3)

            driver.close()
            driver.quit()

            return f"user <{email}> successfully collect coins"
        except:
            return "fail"
