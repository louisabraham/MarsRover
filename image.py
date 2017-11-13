from math import ceil
from collections import namedtuple

import numpy as np
from scipy.signal import fftconvolve

import matplotlib.pyplot as plt

Point = namedtuple('Point', 'x y')


def wheels(f, number=3):
    """
    Returns the coordinates of the centers
    of the wheels

    It uses a convolution on the R image that works
    empirically best (because most of the picture is red)

    Also, could be made a bit faster by providing the previous
    positions (expectancy) and thus calculating the convolution
    on a much smaller image.
    """
    # radius is the parameter of this function
    radius = 15
    # to avoid the water where all is activated,
    # we add negative coefficients to the mask
    # contrast is the value of the positive ones
    # it should be proportional to the radius
    contrast = radius * 2 // 3

    mask_size = int(radius * 2.5)
    mask_center = mask_size // 2
    mask = np.array([[
        10 if
        abs(((i - mask_center) ** 2 + (j - mask_center)**2)**.5 - radius) < 1
        else -1
        for i in range(mask_size)]
        for j in range(mask_size)])
    R = 255 - f[:, :, 0]
    c = fftconvolve(R.astype(int), mask.astype(int), 'same')
    ycenters, xcenters = np.unravel_index(
        c.flatten().argsort()[::-1], f.shape[:2])

    ans = []
    for x, y in zip(xcenters, ycenters):
        # tests if the centers are not too close (describe the same wheel)
        if all(abs(x - xx) + abs(y - yy) > 2 * radius for xx, yy in ans):
            ans.append(Point(x, y))
        if len(ans) == number:
            break
    # we sort to represent the wheels from left to right
    # if it doesn't make sense, then most certainly we are going
    # to lose in the next seconds
    ans.sort()
    return ans


def road(f):
    """
    Returns the shape of the road


    TODO: correct the values given by the argmax using
    the propagation utility function
    TODO: refactor code

    Very fast!
    (https://stackoverflow.com/questions/47240745/extract-colored-line-from-numpy-image)
    """
    range_search = 3
    color_tolerance = 5
    interpolation_limit = 15
    magic = np.array([146, 47, 6])

    limit = f.shape[0]

    ans = (f[:, :, :3] == magic).all(axis=-1).argmax(axis=0).tolist()

    # VERY IMPORTANT, or else the abs fail
    R = f[:, :, 0].astype(int)

    # propagate left
    if ans[0] == 0:
        i = next(i for i in range(len(ans)) if ans[i])
        y = ans[i]
        for i in reversed(range(i)):
            ans[i] = max([y for y in
                          range(ans[i + 1] - range_search,
                                ans[i + 1] + range_search + 1)
                          if abs(R[y + 1, i] - R[y, i]) <= color_tolerance
                          and abs(R[y + 2, i] - R[y, i]) <= color_tolerance],
                         key=lambda y: abs(R[y - 1, i] - R[y, i]),
                         default=ans[i + 1])

    # propagate right
    while 0 in ans:
        i = ans.index(0)
        try:
            j = next(j for j in range(i, len(ans)) if ans[j])
        except StopIteration:
            j = limit
        if j < limit and j - i < interpolation_limit:
            # linear interpolation
            for k in range(i, j):
                ans[k] = ceil(ans[i - 1] + (ans[j] - ans[i - 1]) *
                              (k - i + 1) / (j - i + 1))
        else:
            i -= 1
            while i + 1 < f.shape[0] and not ans[i + 1]:
                i += 1
                ans[i] = max([y for y in
                              range(ans[i - 1] - range_search,
                                    ans[i - 1] + range_search + 1)
                              if abs(R[y + 1, i] - R[y, i]) <= color_tolerance
                              and abs(R[y + 2, i] - R[y, i]) <= color_tolerance],
                             key=lambda y: abs(R[y - 1, i] - R[y, i]),
                             default=ans[i - 1])

    return ans


def demo(f):
    plt.imshow(f)
    plt.scatter(*zip(*wheels(f)), c='b', s=5)
    plt.plot(*zip(*enumerate(road(f))), c='g')


if __name__ == '__main__':
    from scipy import misc
    from time import time

    image = "/tmp/mars.png"

    f = misc.imread(image)

    d = time()
    wheels(f)
    road(f)
    print('%.02f seconds' % (time() - d))
    
    demo(f)
    plt.show()
