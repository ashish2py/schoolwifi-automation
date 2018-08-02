from time import sleep
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedTagNameException, StaleElementReferenceException

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

    def get_media_information(self):
        e = self.driver.find_element_by_css_selector("video")
        v = Video(e)
        print("Width: {0}".format(v.width))
        v.height = 500
        e = self.driver.find_element_by_css_selector("video")
        v = Video(e)

        # check video play
        v.play()
        video_time = int(v.duration())+1
        sleep(video_time)
        if v.current_time == 0:
            print 'VIDEO PLAY DONE'
        else:
            print 'SOME JHOL HAPPEN'

        # check video pause

        print("Height: {0}".format(v.height))
        print("Current Source: {0}".format(v.current_source))
        print("Network State: {0}".format(v.network_state))
        print("Ready State: {0}".format(v.ready_state))
        print("Buffered: {0}".format(v.buffered))
        print("Can Play Type? (video/ogg): {0}".format(v.can_play_type("video/ogg")))
        print("Can Play Type? (video/mp4): {0}".format(v.can_play_type("video/mp4")))
        print("Can Play Type? (video/webm): {0}".format(v.can_play_type("video/webm")))
        print("Seeking: {0}".format(v.seeking))
        print("Duration: {0}".format(v.duration))
        print("Paused?: {0}".format(v.paused))
        print("Played: {0}".format(v.played))
        print("Seekable: {0}".format(v.seekable))
        print("Ended?: {0}".format(v.ended))

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
        self.get_media_information()

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
