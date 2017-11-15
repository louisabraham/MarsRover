from time import sleep

from game import Game
from image import road, wheels
from sensors import slope, proximity_sensors, default_sensor_directions

"""
bugs:
the image processing exception should be treated
more carefully, e.g. by verifying that the game is over
a few moments later, and if it not the case, raising (or logging) the error
with the image
"""


class Executor():

    def __init__(self, driver='PhantomJS', mute=True):
        self.game = Game(driver)
        if mute:
            self.game.mute()

    def inputs(self):
        """
        returns the list of inputs for the controller
        """
        img = self.game.screen()
        r = road(img)
        w = wheels(img)
        return [w[0].x] + [slope(w)] + proximity_sensors(r, w, default_sensor_directions) + self.game._lastcontrols

    def execute(self, controller, timestep=.1, async=True, timeout=20):
        """
        Tests the controller against a full run

        timestep can be 0 because there is a delay
        from the inputs collection (about 300 ms)

        timeout avoids looping because of a null controller
        TODO: timeout in seconds!!! and timestep too!!!
        """
        self.game.restart()
        while not self.game.over():
            if self.game.score() == 0:
                timeout -= 1
            if not timeout:
                return 0
            if not async:
                self.game.pause()
            try:
                inp = self.inputs()
            except Exception as e:
                # raise e
                # print('error', e)
                return self.game.score()
            keys = controller.evaluate(inp)
            self.game.control(*keys)
            # print('\r' + str(keys))
            if not async:
                self.game.resume()
            sleep(timestep)
            # print('\r' + str(game.score()), end='')
        return self.game.score()

    def fit(self, controller, n=2):
        ans = 1
        for _ in range(n):
            ans *= self.execute(controller)
        return ans ** (1 / n)
