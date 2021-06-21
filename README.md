Bot for the [NASA Mars Rover Game](https://mars.nasa.gov/gamee-rover/)
======================================================================

Autonomous cars are a subject of growing interest. Here, we try to pilot
a 2D Mars Rover in **real time** :)

Interface
---------

We use [Selenium](http://www.seleniumhq.org/) to interact with game.

We support the headless WebKit [PhantomJS](http://phantomjs.org/) and
the browsers Chrome and Chromium with the headless option.

Image processing
----------------

We use convolution to retrieve wheels position (blue) and color
detection for the road shape (green).

![image
processing](https://github.com/louisabraham/MarsRover/raw/master/screenshot.png)

References:

-   [Circle
    Detection](http://www.cs.utah.edu/~sshankar/cs6640/project5/circle.html)

Sensors
-------

From the road shape and the wheel position, we simulate some "sensors".

Artificial Intelligence
-----------------------

TODO: Use [SCOOP](https://scoop.readthedocs.io) instead of custom
distributed computations. TODO: Reinforcement learning? Or implement
[Evolution Strategies as a Scalable Alternative to Reinforcement
Learning](https://arxiv.org/abs/1703.03864). See also
[RLlib](https://ray.readthedocs.io/en/latest/rllib.html) and https://eng.uber.com/deep-neuroevolution/.

We use genetic evolved neural networks. It doesn't work very well
(tested the 1+4+1 strategy over 50 generations).

We can increase the speed of our program by evaluating the controllers
in parallel in a SLURM cluster, see `main_distributed.py`.
