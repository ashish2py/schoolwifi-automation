from time import sleep
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import requests


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://wifi.zaya.in/#/dashboard")
        self.webserver = 'http://wifi.zaya.in/#/dashboard'

    # timer/sleep with counter
    def let_me_sleep(self, time):
        for counter in range(time):
            sys.stdout.write("\rWAITING FOR {}/{}  :: ".format(counter + 1, time))
            sys.stdout.flush()
            sleep(counter)
        print ('\n')

    # swtich to iframe content
    def switch_to_iframe_by_xpath(self, element_key):
        self.driver.switch_to.frame(self.driver.find_element_by_xpath(element_key))

    # swtich to default content
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    # make head request and prepare a passed and failed requests
    def head_request_report(self, requests):
        pass

    def get_current_url(self):
        return self.driver.get_current_url

    def check_video(self):
        pass

    ##############################
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

        # 1
        element = self.driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div/\
                                                     div[2]/div/div/ul/li[{}]'.format(counter + 1))
        print('PLAYING #{}/{}'.format(counter, element.text))
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

    ################################################
    #  PAGINATION
    #  TODO : Better way to handle pagination
    ################################################
    def calculate_page(self):
        pagination_pages = self.driver.find_elements_by_css_selector('.pagination-page.ng-scope')
        # print('PAGES #{}'.format(pagination_pages[-1].text))
        return pagination_pages

    def check_next_button_active(self):
        if not self.driver.find_elements_by_css_selector('.pagination-next.ng-scope.disabled'):
            next_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div/div/div[1]/div/div/div[3]/ul/li[9]/a')))
            return next_button
        return False

    # JUGAAD
    def multiple_button_click(self, counter, item):
        self.let_me_sleep(2)
        for click in range(counter):
            item.click()

    def click_next_button(self):
        import ipdb;ipdb.set_trace()
        number_of_pages = self.calculate_page()

        for index, page in enumerate(number_of_pages):
            next_button_active = self.check_next_button_active()
            if next_button_active:
                self.multiple_button_click(index + 1, next_button_active)
            continue

    ##############################
    #   FILTERS
    ##############################
    def searchbar_filter_check(self):
        ''' SEND input to searchbar '''
        search_bar = self.driver.find_elements_by_css_selector(
            '.form-control.ng-pristine.ng-valid.ng-empty.ng-touched')
        if search_bar:
            search_bar[0].click()
            search_bar[0].send_keys('Grammar')
            self.let_me_sleep(2)
            search_result = self.driver.find_elements_by_css_selector('.media-heading.ng-binding')
            self.assertTrue('Grammar' in search_result[0].text)

    def grade_filter(self):
        pass

    def skill_filter(self):
        pass

    def title_filter(self):
        pass

    def check_filters(self):
        ''' Search filter '''
        tbody_available = self.driver.find_elements_by_xpath(
            '/html/body/div/div/div[1]/div/div/div[1]/div/div/div[2]/table/tbody')
        if tbody_available:
            tbody = tbody_available[0]
            tbody_trs = tbody.find_elements_by_tag_name('tr')
            for tr in tbody_trs:
                tr_tds = tr.find_elements_by_tag_name('td')
                for td in tr_tds:
                    # print(td.text)
                    # TODO : Add id/class to input-search-bar or name to avoid string comparision
                    # SEARCH Filter
                    if td.text is '':
                        # print('SEARCH FILTER')
                        td.click()
                        # click search bar
                        self.driver.find_element_by_css_selector(
                            '.form-control.ng-pristine.ng-valid.ng-empty.ng-untouched').click()
                        self.let_me_sleep(2)
                        self.searchbar_filter_check()

                    # TODO : Grade filter
                    # TODO : Skill filter
        else:
            print('SEARCH FIELD NOT AVAILABLE')

    ##############################
    # FILTERS
    ##############################

    # @unittest.skip("zaya apps")
    def test_000_zaya_applications(self):
        print('---------------------------------------------------------------------------------------------')
        print('TESTING ZAYA APP OVER {}. MAKE SURE YOUR ARE CONNECTED TO BOX/INTERNET!!'.format(self.webserver))
        print('---------------------------------------------------------------------------------------------')
        self.driver.get(self.webserver)     # add your webserver/website name
        self.let_me_sleep(6)

        application_elements = self.driver.find_elements_by_class_name('app-block')
        application_count = len(application_elements) + 1
        for app_counter in range(application_count):
            sleep(2)
            _application_elements = self.driver.find_elements_by_class_name('app-block')
            _application_elements[app_counter].click()
            _application_name = self.driver.find_element_by_class_name('page-title')
            print ('APP TESTING #', _application_name.text)

            # check availability of iframe and switch
            iframe_available = self.driver.find_elements_by_xpath('//*[@id="loaded"]')
            if iframe_available:
                self.switch_to_iframe_by_xpath('//*[@id="loaded"]')
            else:
                print('APPLICATION TAKING TIME TO LOAD')
                continue

            # test filters
            # self.check_filters()

            self.click_next_button() 

            # list_elements = self.get_media_list()
            # len_elements = len(list_elements)
            # print ('MEDIA FILES TO BE TESTED #', str(len_elements))

            # # open list
            # try:
            #     for key, source in enumerate(list_elements):
            #         self.open_media_content(key)
            #         self.let_me_sleep(3)
            #         if key + 1 == len_elements:
            #             self.switch_to_default_content()
            # except Exception as e:
            #     print('Exception occurs' + str(e))
            #     pass

            self.switch_to_default_content()

    def tearDown(self):
        self.driver.close()

    # def test_111_switch_applications(self):
    #     sleep(5)
    #     application_elements = self.driver.find_elements_by_class_name('app-block')
    #     application_count = len(application_elements) + 1
    #     for app_counter in range(application_count):
    #         sleep(2)
    #         _application_elements = self.driver.find_elements_by_class_name('app-block')
    #         _application_elements[app_counter].click()
    #         _application_name = self.driver.find_element_by_class_name('page-title')
    #         print ('APP TESTING #', _application_name.text)
    #         sleep(4)
    #         self.goBack()

    def goBack(self):
        self.driver.execute_script("window.history.go(-1)")


if __name__ == "__main__":
    unittest.main()
