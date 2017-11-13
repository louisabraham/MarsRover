# Bot for the [NASA Mars Rover Game](https://mars.nasa.gov/gamee-rover/)

Autonomous cars are a subject of growing interest. Here, we try to pilot a 2D Mars Rover in **real time** :)

## Interface

We use [Selenium](http://www.seleniumhq.org/) to interact with game.

We support the headless WebKit [PhantomJS](http://phantomjs.org/) and the browsers Chrome and Chromium with the headless option.

## Image processing

We use convolution to retrieve wheels position (blue) and color detection for the road shape (green).

![image processing](https://github.com/louisabraham/MarsRover/raw/master/screenshot.png)

References:

- [Circle Detection](http://www.cs.utah.edu/~sshankar/cs6640/project5/circle.html)

## Sensors

From the road shape and the wheel position, we simulate some "sensors".

## Artificial Intelligence

TODO: Reinforcement learning?

We use genetic evolved neural networks. It doesn't work very well (tested the 1+4+1 strategy over 50 generations).

TODO: Distributed evaluation of the neural networks using HTTP GET servers with serialized inputs.