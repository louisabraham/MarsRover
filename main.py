from time import sleep

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
    from the inputs collection (about 320 ms)
    
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
        keys = controller.evaluate(inputs(game))
        game.control(*keys)
        # print('\r' + str(keys))
        if not async:
            game.resume()
        sleep(timestep)
    return game.score()

if __name__ == '__main__':
    game = Game('chrome')
    game.mute()
    d = time();inputs();print(time()-d)
    controller = controllerNN([16, 32, 32, 6])
    execute(game, controller)
    