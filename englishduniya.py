from time import sleep
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import requests


class SchoolWifiTestSuite(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    # timer/sleep with counter
    def let_me_sleep(self, time):
        # for counter in range(time):
            # sys.stdout.write("\rWAITING FOR {}/{}  :: ".format(counter + 1, time))
            # sys.stdout.flush()
            # sleep(counter)
        sleep(time)
        # print ('\n')

    # paginaction
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

    def click_next_button_and_play_video(self):
        number_of_pages = self.calculate_page()
        number_of_pages = int(number_of_pages[-1].text) - 1
        print (number_of_pages)
        for page in range(number_of_pages):
            print ('\n\nPAGE #', page + 1)
            next_button_active = self.check_next_button_active()
            if next_button_active:
                played_batch = self.list_and_play_videos()
                if played_batch:
                    next_button_active = self.check_next_button_active()
                    next_button_active.click()
                else:
                    print ('FAILED while playing video in pagination')
            continue
    # end of paginaction

    # media files
    def get_media_list(self):
        ''' CALCULATE MEDIA LIST on iframe'''
        self.calculate_page()
        list_elements = self.driver.find_elements_by_css_selector('.media.pointer.ng-scope')
        return list_elements

    def open_media_content(self, counter):
        '''
        MEDIA CONTENT CHECK AVAILABILITY
        1. click on media content list.
        2. look for VIDEO tag and check for SRC attribute.
        3. check media files availability.
        4. if not available then log into error log and return false.
        5. if availabel then log it as a succesfull.  '''
        self.let_me_sleep(2)
        print ('\n')

        # 1
        element = self.driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div/\
                                                     div[2]/div/div/ul/li[{}]'.format(counter + 1))
        print('PLAYING #{}/{}'.format(counter + 1, element.text))
        element.click()
        self.let_me_sleep(3)

        # 2
        # check media file availability by making HEADE request to media file.
        video_url = self.driver.find_element_by_tag_name('video').get_attribute('src')

        # 3
        request = requests.head(video_url)
        if request.status_code == 200:
            # 4 TODO : log success
            print ('SIZE ', request.headers.get('Content-Length'))
            print('SUCCESS : media file is available')
        else:
            # 5 TODO : log faiure and return FALSE
            print('ERROR : media file is unavailable')

        # Go Back
        self.driver.find_element_by_css_selector('.btn.btn-danger').click()

    def list_and_play_videos(self):
        list_media_files = self.get_media_list()
        len_elements = len(list_media_files)
        print ('MEDIA FILES TO BE TESTED #', str(len_elements))

        # open list
        try:
            for key, source in enumerate(list_media_files):
                self.open_media_content(key)
                self.let_me_sleep(2)
            return True
        except Exception as e:
            print('Exception occurs' + str(e))
            return False
    # end of media files

    # test case
    def test_01_englishduniya(self):
        self.driver.get("http://sws-englishduniya.zaya.in/")
        sleep(5)
        self.click_next_button_and_play_video()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
