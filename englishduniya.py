from time import sleep
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys


class SchoolWifiTestSuite(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    # timer/sleep with counter
    def let_me_sleep(self, time):
        for counter in range(time):
            sys.stdout.write("\rWAITING FOR {}/{}  :: ".format(counter + 1, time))
            sys.stdout.flush()
            sleep(counter)
        print ('\n')

    def calculate_page(self):
        pagination_pages = self.driver.find_elements_by_css_selector('.pagination-page.ng-scope')
        # print('PAGES #{}'.format(pagination_pages[-1].text))
        return pagination_pages

    def check_next_button_active(self):
        if not self.driver.find_elements_by_css_selector('.pagination-next.ng-scope.disabled'):
            next_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Next')]")))
            # self.driver.find_elements_by_xpath()[-1]
            return next_button
        return False

    def click_next_button(self):
        number_of_pages = self.calculate_page()
        number_of_pages = int(number_of_pages[-1].text) - 1
        print (number_of_pages)
        for page in range(number_of_pages):
            print ('PAGE #',page+1)
            next_button_active = self.check_next_button_active()
            if next_button_active:
                self.let_me_sleep(3)
                next_button_active.click()
            continue

    def test_01_englishduniya(self):
        self.driver.get("http://sw-englishduniya.zaya.in/")
        sleep(5)
        self.click_next_button()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
