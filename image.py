import numpy as np
from scipy.signal import convolve2d


def wheels(f, number=3):
    """
    Returns the coordinates of the centers
    of the wheels

    It uses a convolution on the R image
    that works empirically best

    Works on the 256x256 and 512x512 images

    Could be improved by expecting the resulting
    points to be approximatively aligned and not too close
    Also, could be made much faster by providing the previous
    positions (expectancy) and thus calculating the convolution
    on a much smaller image.
    """
    res = f.shape[0]
    radius = 6 * res // 256
    mask_size = int(radius * 2.5)
    mask_center = mask_size // 2
    mask = np.array([[
        abs(((i - mask_center) ** 2 + (j - mask_center)**2)**.5 - radius) < 1
        for i in range(mask_size)]
        for j in range(mask_size)])

    R = 255 - f[:, :, 0]
    c = convolve2d(R.astype(int), mask.astype(int), 'same')
    ycenters, xcenters = np.unravel_index(
        c.flatten().argsort()[-number:], (res, res))
    return list(zip(xcenters, ycenters))

def road(f):
    """
    Returns the shape of the road
    
    Could be made faster using vectorized operations
    """
    res = f.shape[0]
    magic = 146, 47, 6
    return [min(l for l in range(res) if np.array_equal(magic, f[l, c, :3])) for c in range(res)]
    
if __name__ == '__main__':
    from scipy import misc
    import matplotlib.pyplot as plt

    image = "/Users/louisabraham/github/MarsRover/256.png"
    f = misc.imread(image)

    plt.imshow(f, cmap='gray')
    plt.scatter(*zip(*wheels(f)), c='b', s=5)
    plt.plot(range(f.shape[0]), road(f), c='g')
    plt.show()
