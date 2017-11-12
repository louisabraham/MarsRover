import numpy as np
import numpy.random as rnd
from collections import namedtuple


MUTATION_PARAM = 5


class SimpleNN(namedtuple("SimpleNN", 'W, C')):

    def __new__(cls, *args):
        if len(args) == 1:
            layers, = args
            W = [rnd.standard_normal((i, j))
                 for i, j in zip(layers[:-1], layers[1:])]
            C = rnd.standard_normal(len(layers) - 1)
        else:
            W, C = args
        return super().__new__(cls, W, C)

    def evaluate(self, inp):
        for w, c in zip(*self):
            inp = max(0, np.dot(inp, w) + c)
        return inp

    @staticmethod
    def aux_reproduce(a, b, MUTATION_PARAM):
        assert a.shape == b.shape
        shape = a.shape
        mean = (a + b).flatten() / 2
        cov = np.diag(np.abs(a - b).flatten() * MUTATION_PARAM)
        return np.reshape(rnd.multivariate_normal(mean, cov), shape)

    def reproduce(a, b, MUTATION_PARAM=MUTATION_PARAM):
        assert len(a.W) == len(b.W)
        W = [SimpleNN.aux_reproduce(wa, wb, MUTATION_PARAM)
             for wa, wb in zip(a.W, b.W)]
        C = SimpleNN.aux_reproduce(a.C, b.C, MUTATION_PARAM)
        return SimpleNN(W, C)


class controllerNN(SimpleNN):

    def __init__(self, *args):
        if len(args) == 1:
            layers, = args
            assert layers[-1] == 6
        else:
            W, C = args
            assert W[-1].shape[1] == 6

    def evaluate(self, inp):
        ans = super().evaluate(inp)
        return np.argmax(ans[:3]) - 1, np.argmax(ans[3:]) - 1

if __name__ == '__main__':

    from itertools import product
    from time import time

    MUT = 5

    dbt = time()

    X = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])

    y = np.array([[0, 1, 1, 0]])

    def fit(nn):
        return -((y - nn.evaluate(X).T)**2).sum()

    l = [SimpleNN([3, 4, 1]) for i in range(100)]

    for _ in range(20):

        l.sort(key=fit, reverse=True)
        pool = l[:10]
        l = []
        for i, j in product(pool, repeat=2):
            l.append(i.reproduce(j, MUT))

    l.sort(key=fit, reverse=True)
    print('%.02f seconds' % (time() - dbt))
    print(MUT, fit(l[0]), l[0].evaluate(X))
