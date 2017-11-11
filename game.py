from time import sleep
from os import system
import io

from selenium import webdriver
from scipy import misc
import matplotlib.pyplot as plt
# from selenium.webdriver.common.keys import Keys

from image import wheels, road, demo as image_demo

URL = "https://d29zfk7accxxr5.cloudfront.net/games/game-142/data/index.html"
RESOLUTION = 512


class Game():

    def __init__(self, res=RESOLUTION):
        # TODO: use chromedriver with or without headless
        # (https://intoli.com/blog/running-selenium-with-headless-chrome/)
        
        # --disk-cache=true allows to keep a cache
        driver = webdriver.PhantomJS(service_args=['--disk-cache=true'])
        driver.set_window_size(res, res)
        driver.get(URL)
        body = driver.switch_to_active_element()
        sleep(.2)
        self.driver = driver
        self.body = body

    def start(self):
        self.body.send_keys('r')

    def screen(self, file=None):
        """
        Does a screenshot

        By default, returns the screen as png, the wheels and the road.
        screen(True) displays the processed screen
        screen(file) saves the screen
        """
        f = misc.imread(io.BytesIO(self.driver.get_screenshot_as_png()))
        if file is None:
            return f, wheels(f), road(f)
        elif file is True:
            image_demo(f)
            plt.savefig('/tmp/screenMars.png')
            system('open /tmp/screenMars.png')
        else:
            self.driver.save_screenshot(file)
