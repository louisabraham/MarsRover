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
        if len(ans) == 3:
            break
    # we sort to represent the wheels from left to right
    # if it doesn't make sense, then most certainly we are going
    # to lose in the next seconds
    ans.sort()
    return ans


def road(f):
    """
    Returns the shape of the road

    FAILS when an
    TODO: implement closest match amongst neighbors
    idea: convolve (artificially and locally) the red layer with
    [[0, 1, 0], [1, -4, 1], [0, 1, 0]] and take the heighest neighbour of value less than 10
    or [[0, 1, 0], [0, -2, 0], [0, 1, 0]]

    Very fast!
    (https://stackoverflow.com/questions/47240745/extract-colored-line-from-numpy-image)
    """
    range_search = 2
    color_tolerance = 10
    magic = np.array([146, 47, 6])

    ans = (f[:, :, :3] == magic).all(axis=-1).argmax(axis=0).tolist()

    R = f[:, :, 0]

    # propagate left
    if ans[0] == 0:
        j = next(j for j in range(len(ans)) if ans[j])
        y = ans[j]
        while j:
            j -= 1
            y = y + range_search
            for _ in range(2 * range_search + 1):
                y -= 1
                if abs(2 * f[y, j, 0] - f[y+1, j, 0] - f[y-1, j, 0]) > color_tolerance:
                    y += 1
                    break
            ans[j] = y
    
    # propagate right
    # TODO: interpolate linearly when gap is sufficiently small
    while 0 in ans:
        j = ans.index(0) - 1
        y = ans[j]
        while j < f.shape[0] - 1 and not ans[j + 1]:
            j += 1
            y = y + range_search
            for _ in range(2 * range_search + 1):
                y -= 1
                if abs(2 * f[y, j, 0] - f[y+1, j, 0] - f[y-1, j, 0]) > color_tolerance:
                    y += 1
                    break
            ans[j] = y
    
    # # when we find water, the color changes so
    # # we interpolate the shape of the road linearly
    # while 0 in ans:
    #     i = ans.index(0)
    #     # the last pixel before the water might be of
    #     # a different color, we allow some tolerance
    #     while abs(f[ans[i - 1] - 1, i - 1, :3] - magic).max() <= color_tolerance:
    #         ans[i - 1] -= 1
    #     j = next(j for j in range(i, len(ans)) if ans[j])
    #     for k in range(i, j):
    #         ans[k] = ceil(ans[i - 1] + (ans[j] - ans[i - 1]) *
    #                       (k - i + 1) / (j - i + 1))
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
