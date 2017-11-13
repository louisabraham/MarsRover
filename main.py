from time import sleep
from itertools import product

import numpy as np

from game import Game
from GNN import controllerNN
from image import road, wheels
from sensors import slope, proximity_sensors, default_sensor_directions


def inputs(game):
    """
    returns the list of inputs for the controller
    """
    img = game.screen()
    r = road(img)
    w = wheels(img)
    return [slope(w)] + proximity_sensors(r, w, default_sensor_directions) + game._lastcontrols


def execute(game, controller, timestep=0, async=True, timeout=10):
    """
    Tests the controller against a full run

    timestep can be 0 because there is a delay
    from the inputs collection (about 300 ms)

    timeout avoids looping because of a null controller
    """
    game.restart()
    while not game.over():
        if game.score() == 0:
            timeout -= 1
        if not timeout:
            return 0
        if not async:
            game.pause()
        try:
            inp = inputs(game)
        except Exception as e:
            # print('error', e)
            return game.score()
        keys = controller.evaluate(inp)
        game.control(*keys)
        # print('\r' + str(keys))
        if not async:
            game.resume()
        sleep(timestep)
        # print('\r' + str(game.score()), end='')
    return game.score()

if __name__ == '__main__':
    game = Game('chrome')
    game.mute()

    def fit(controller):
        return sum(execute(game, controller) for _ in range(2)) / 2

    def new():
        return controllerNN([16, 8, 8, 6], activation='sigmoid')

    best = new()
    while not fit(best):
        best = new()

    for gen in range(50):
        pop = [best] + [best.mutate() for _ in range(4)] + [new()]
        scores = list(map(fit, pop))
        print('gen %s :' % gen, scores)
        best = pop[np.argsort(scores)[-1]]

    print(scores)
