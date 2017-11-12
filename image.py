from math import ceil

import numpy as np
from scipy.signal import fftconvolve

import matplotlib.pyplot as plt


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

    mask_size = int(radius * 2.5)
    mask_center = mask_size // 2
    mask = np.array([[
        abs(((i - mask_center) ** 2 + (j - mask_center)**2)**.5 - radius) < 1
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
            ans.append((x, y))
    # we sort to represent the wheels from left to right
    # if it doesn't make sense, then most certainly we are going
    # to lose in the next seconds
    ans.sort()
    return ans


def road(f):
    """
    Returns the shape of the road

    Very fast!
    (https://stackoverflow.com/questions/47240745/extract-colored-line-from-numpy-image)
    """
    magic = np.array([146, 47, 6])
    color_tolerance = 3

    ans = (f[:, :, :3] == magic).all(axis=-1).argmax(axis=0).tolist()

    # when we find water, the color changes
    while 0 in ans:
        i = ans.index(0)
        while abs(f[ans[i - 1] - 1, i - 1, :3] - magic).max() <= color_tolerance:
            ans[i - 1] -= 1
        j = next(j for j in range(i, len(ans)) if ans[j])
        for k in range(i, j):
            ans[k] = ceil(ans[i - 1] + (ans[j] - ans[i - 1]) *
                          (k - i + 1) / (j - i + 1))
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
