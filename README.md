# Bot for the [NASA Mars Rover Game](https://mars.nasa.gov/gamee-rover/)

Autonomous cars are a subject of growing interest. Here, we try to pilot a 2D Mars Rover in **real time** :)

## Interface

We use [Selenium](http://www.seleniumhq.org/) to interact with game.

We support the headless WebKit [PhantomJS](http://phantomjs.org/) and the browsers Chrome and Chromium with the headless option.

## Image processing

We use image processing to retrieve the road shape (green) and the wheels position (blue).

![image processing](https://github.com/louisabraham/MarsRover/blob/master/screenshot.png?raw=true)

References:

- [Circle Detection](http://www.cs.utah.edu/~sshankar/cs6640/project5/circle.html)

## Artificial Intelligence

Reinforcement learning, genetic algorithm?