URL = "https://d29zfk7accxxr5.cloudfront.net/games/game-142/data/index.html"
RESOLUTION = 512

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from os import system


class Game():

    def __init__(self, res=RESOLUTION):
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
        if file is None:
            return self.driver.get_screenshot_as_png()
        elif file is True:
            self.driver.save_screenshot('/tmp/screenMars.png')
            system('open /tmp/screenMars.png')
        else:
            self.driver.save_screenshot(file)

if __name__ == '__main__':
    game = Game()
    game.start()
    game.screen(True)
