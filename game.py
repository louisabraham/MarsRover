from time import sleep
import io
import base64
from hashlib import md5

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from scipy import misc


URL = "https://d29zfk7accxxr5.cloudfront.net/games/game-142/data/index.html"


class Game():

    def __init__(self, driver):
        driver = driver.casefold()

        if driver == 'phantomjs':
            # --disk-cache=true allows to keep a cache
            self.driver = webdriver.PhantomJS(
                service_args=['--disk-cache=true'])

        elif driver in ['chrome', 'chrome-headless', 'chromium', 'chromium-headless']:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--disable-gpu")  # most important line
            chrome_options.add_argument("--disable-extensions")            
            if len(driver.split('-')) == 2:
                chrome_options.add_argument("--headless")
            if driver.split('-')[0] == 'chromium':
                chrome_options.binary_location = '/Applications/Chromium.app/Contents/MacOS/Chromium'
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

        elif driver == 'firefox':
            # not working, disable gpu?
            self.driver = webdriver.Firefox()

        self.driver.get(URL)

        # hash of starting screen
        magic = '2979145a2e1a7685c995a8e097276cd1'
        while self.screen_hash() != magic:
            sleep(.1)
            # print(self.screen_hash())

        self.driver.switch_to_active_element().send_keys('r')

    def screen(self, file=None):
        """
        Does a screenshot

        returns the screen
        """
        data = self.driver.execute_script(
            "return document.getElementById('canvas').toDataURL()")[22:]
        data = base64.b64decode(data)
        img = misc.imread(io.BytesIO(data))
        misc.imsave('/tmp/mars.png', img)
        return img

    def screen_hash(self):
        """
        return hash of screen
        """
        return md5(bytes(self.screen())).digest().hex()

    def restart(self):
        self.driver.execute_script('gamee.onRestart()')

    def pause(self):
        self.driver.execute_script('gamee.onPause()')

    def mute(self):
        self.driver.execute_script('gamee.onMute()')

    def resume(self):
        self.driver.execute_script('gamee.onResume()')

    def score(self):
        'can do more accurate'
        return self.driver.execute_script('return gamee.score')

    def over(self):
        return self.screen_hash() == '3f0371f975116bb1165834d64c4c67b0'

    def control(self, updown, leftright):
        controls = ['keyup', 'keydown']
        command = """
        gamee.controller.trigger("%s", {button : "left"});
        gamee.controller.trigger("%s", {button : "right"});
        gamee.controller.trigger("%s", {button : "down"});
        gamee.controller.trigger("%s", {button : "up"});
        """
        params = (controls[leftright == -1],
                  controls[leftright == 1],
                  controls[updown == -1],
                  controls[updown == 1])
        self.driver.execute_script(command % params)
