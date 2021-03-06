from time import sleep
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

import sys
import requests



def stale(fn):
    def wrapper(self, *args):
        if self.changed:
            raise StaleElementReferenceException()
        return fn(self, *args)
    return wrapper

class HTML5Media(object):
    # error state
    @property
    def error(self):
        if self.changed:
            raise StaleElementReferenceException()
        errors = {
            1: "MEDIA_ERR_ABORTED",
            2: "MEDIA_ERR_NETWORK",
            3: "MEDIA_ERR_DECODE",
            4: "MEDIA_ERR_SRC_NOT_SUPPORTED"
        }
        return errors[self._el._parent.execute_script("return arguments[0].error", self._el)]
    
    # network state
    @property
    @stale
    def src(self):
        return self._el._parent.execute_script("return arguments[0].src", self._el)

    @src.setter
    def src(self, value):
        if isinstance(value, str):
            self._el._parent.execute_script("arguments[0].src = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a string")

    @property
    @stale
    def current_source(self):
        """Returns the current source of the video"""
        return self._el._parent.execute_script("return arguments[0].currentSrc", self._el)

    @property
    @stale
    def cross_origin(self):
        return self._el._parent.execute_script("return arguments[0].crossOrigin", self._el)

    @cross_origin.setter
    def cross_origin(self, value):
        if isinstance(value, str):
            self._el._parent.execute_script("arguments[0].crossOrigin = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a string")

    @property
    @stale
    def network_state(self):
        """Returns the string representation of the current network state"""
        states = {
            0: "NETWORK_EMPTY",
            1: "NETWORK_IDLE",
            2: "NETWORK_LOADING",
            3: "NETWORK_NO_SOURCE",
        }
        return states[self._el._parent.execute_script("return arguments[0].networkState", self._el)]

    @property
    @stale
    def preload(self):
        return self._el._parent.execute_script("return arguments[0].preload", self._el)

    @preload.setter
    def preload(self, value):
        if value in ["none", "metadata", "auto"]:
            self._el._parent.execute_script("arguments[0].preload = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be either 'none', 'metadata' or 'auto'")

    @property
    @stale
    def buffered(self):
        """Returns the current source of the video"""
        return self._el._parent.execute_script("return arguments[0].buffered", self._el)

    @stale
    def load(self):
        self._el._parent.execute_script("arguments[0].load()", self._el)

    @stale
    def can_play_type(self, media_type):
        return self._el._parent.execute_script("return arguments[0].canPlayType(arguments[1])", self._el, media_type)

    # ready state
    @property
    @stale
    def ready_state(self):
        states = {
            0: "HAVE_NOTHING",
            1: "HAVE_METADATA",
            2: "HAVE_CURRENT_DATA",
            3: "HAVE_FUTURE_DATA",
            4: "HAVE_ENOUGH_DATA"
        }
        return states[self._el._parent.execute_script("return arguments[0].readyState", self._el)]

    @property
    @stale
    def seeking(self):
        return self._el._parent.execute_script("return arguments[0].seeking", self._el)
    
    # playback state
    @property
    @stale
    def current_time(self):
        return self._el._parent.execute_script("return arguments[0].currentTime", self._el)

    @current_time.setter
    def current_time(self, value):
        if isinstance(value, int):
            self._el._parent.execute_script("arguments[0].currentTime = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a boolean")

    @property
    @stale
    def initial_time(self):
        return self._el._parent.execute_script("return arguments[0].initialTime", self._el)
    
    @property
    @stale
    def duration(self):
        return self._el._parent.execute_script("return arguments[0].duration", self._el)

    @property
    @stale
    def start_offset_time(self):
        return self._el._parent.execute_script("return arguments[0].startOffsetTime", self._el)

    @property
    @stale
    def paused(self):
        return self._el._parent.execute_script("return arguments[0].paused", self._el)

    @property
    @stale
    def default_playback_rate(self):
        return self._el._parent.execute_script("return arguments[0].defaultPlaybackRate", self._el)

    @default_playback_rate.setter
    def default_playback_rate(self, value):
        if isinstance(value, int):
            self._el._parent.execute_script("arguments[0].defaultPlaybackRate = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a int")

    @property
    @stale
    def playback_rate(self):
        return self._el._parent.execute_script("return arguments[0].playbackRate", self._el)

    @playback_rate.setter
    def playback_rate(self, value):
        if isinstance(value, int):
            self._el._parent.execute_script("arguments[0].playbackRate = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a int")

    @property
    @stale
    def played(self):
        return self._el._parent.execute_script("return arguments[0].played", self._el)

    @property
    @stale
    def seekable(self):
        return self._el._parent.execute_script("return arguments[0].seekable", self._el)

    @property
    @stale
    def ended(self):
        return self._el._parent.execute_script("return arguments[0].ended", self._el)

    @property
    @stale
    def autoplay(self):
        return self._el._parent.execute_script("return arguments[0].autoplay", self._el)

    @autoplay.setter
    def autoplay(self, value):
        if isinstance(value, bool):
            self._el._parent.execute_script("arguments[0].autoplay = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a boolean")

    @property
    @stale
    def loop(self):
        return self._el._parent.execute_script("return arguments[0].loop", self._el)

    @loop.setter
    def loop(self, value):
        if isinstance(value, bool):
            self._el._parent.execute_script("arguments[0].loop = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a boolean")

    @stale
    def play(self):
        x = self._el._parent.execute_script("arguments[0].play()", self._el)

    @stale
    def pause(self):
        x = self._el._parent.execute_script("arguments[0].pause()", self._el)

    # media controller
    @property
    @stale
    def mediagroup(self):
        return self._el._parent.execute_script("return arguments[0].mediagroup", self._el)

    @mediagroup.setter
    def mediagroup(self, value):
        if isinstance(value, str):
            self._el._parent.execute_script("arguments[0].mediagroup = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a string")

    # controls
    @property
    @stale
    def controls(self):
        return self._el._parent.execute_script("return arguments[0].controls", self._el)

    @controls.setter
    def controls(self, value):
        if isinstance(value, bool):
            self._el._parent.execute_script("arguments[0].controls = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a boolean")

    @property
    @stale
    def volume(self):
        return self._el._parent.execute_script("return arguments[0].volume", self._el)

    @volume.setter
    def volume(self, value):
        if isinstance(value, int):
            self._el._parent.execute_script("arguments[0].volume = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a int")

    @property
    @stale
    def muted(self):
        return self._el._parent.execute_script("return arguments[0].muted", self._el)

    @muted.setter
    def muted(self, value):
        if isinstance(value, bool):
            self._el._parent.execute_script("arguments[0].muted = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a boolean")

    @property
    @stale
    def default_muted(self):
        return self._el._parent.execute_script("return arguments[0].defaultMuted", self._el)

    @default_muted.setter
    def default_muted(self, value):
        if isinstance(value, bool):
            self._el._parent.execute_script("arguments[0].defaultMuted = arguments[1]", self._el, value)
            self.changed = True
        else:
            raise ValueError("value needs to be a boolean")

class Video(HTML5Media):
    def __init__(self, webelement):
        """
        Constructor. A check is made that the given element is, indeed, a VIDEO tag. If it is not,
        then an UnexpectedTagNameException is thrown.

        :Args:
         - webelement - element VIDEO element to wrap
        
        Example:
            from selenium.webdriver.support.ui import Select \n
            Video(driver.find_element_by_tag_name("video")).play()
        """
        if webelement.tag_name.lower() != "video":
            raise UnexpectedTagNameException(
                "Video only works on <video> elements, not on <%s>" % 
                webelement.tag_name)
        self._el = webelement
        self.changed = False

    @property
    @stale
    def width(self):
        """Returns the width in px of the video"""
        return self._el._parent.execute_script("return arguments[0].width", self._el)

    @width.setter
    def width(self, value):
        """Sets the width in px of the video"""
        self._el._parent.execute_script("arguments[0].width = arguments[1]", self._el, value)
        self.changed = True

    @property
    @stale    
    def video_width(self):
        """Returns the width in px of the video"""
        return self._el._parent.execute_script("return arguments[0].videoWidth", self._el)

    @property
    @stale
    def height(self):
        """Returns the height in px of the video"""
        return self._el._parent.execute_script("return arguments[0].height", self._el)

    @height.setter
    def height(self, value):
        """Sets the width in px of the video"""
        self._el._parent.execute_script("arguments[0].height = arguments[1]", self._el, value)
        self.changed = True

    @property
    @stale
    def video_height(self):
        """Returns the height in px of the video"""
        return self._el._parent.execute_script("return arguments[0].videoHeight", self._el)

    @property
    @stale
    def poster(self):
        return self._el._parent.execute_script("return arguments[0].poster", self._el)

    @poster.setter
    def poster(self, value):
        self._el._parent.execute_script("arguments[0].poster = arguments[1]", self._el, value)
        self.changed = True

class Audio(HTML5Media):
    def __init__(self, webelement):
        """
        Constructor. A check is made that the given element is, indeed, a Audio tag. If it is not,
        then an UnexpectedTagNameException is thrown.

        :Args:
         - webelement - element Audio element to wrap

        Example:
            from selenium.webdriver.support.ui import Select \n
            Audi(driver.find_element_by_tag_name("audio")).play()
        """
        if webelement.tag_name.lower() != "audio":
            raise UnexpectedTagNameException(
                "Audio only works on <audio> elements, not on <%s>" % 
                webelement.tag_name)
        self._el = webelement
        self.changed = False


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
