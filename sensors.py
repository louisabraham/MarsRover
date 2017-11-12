"""
We do some *feature engineering* to simulate sensors
"""

from math import exp, hypot, pi, cos, sin

from image import Point


def slope(w):
    """
    returns the slope of the rover
    """
    a, b, c = w
    return (a.y - c.y) / (c.x - a.x + 1e-9)


def proximity(point, road, vector, activation=lambda x: exp(-x)):
    """
    returns an activated distance
    between the point and the road
    when following the vector
    """
    n = len(road)
    y = lambda c: point.y - (vector.y / vector.x) * (c - point.x)
    if vector.x > 0:
        try:
            c = next(c for c in range(point.x, n) if y(c) - road[c] < 1)
        except StopIteration:
            return 0
    elif vector.x < 0:
        try:
            c = next(c for c in range(point.x, -1, -1) if y(c) - road[c] < 1)
        except StopIteration:
            return 0
    else:
        if vector.y > 0:
            return activation(road[point.x] - point.y)
        else:
            return 0
    return hypot(c - point.x, road[c] - point.y)


def proximity_sensors(road, sensors, sensor_directions):
    """
    road is the road
    sensor is a list of sensor coordinated
    params contains one list for each sensor
    each list contains the proximity sensors vectors

    returns the list of sensors outputs
    """
    return [proximity(sensor, road, vector) for sensor, l in zip(sensors, sensor_directions) for vector in l]


def direction(t):
    """
    sensor direction vector with angle t
    from vertical vector
    """
    return Point(sin(t), cos(t))

default_sensor_directions = [
    [
        direction(-pi / 6),
        direction(0),
        direction(pi / 6)
    ],
    [
        direction(-pi / 6),
        direction(0),
        direction(pi / 6)
    ],
    [direction(i * pi / 8) for i in range(-1, 6)]
]
