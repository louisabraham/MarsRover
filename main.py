from itertools import product

import numpy as np

from GNN import controllerNN

from executor import Executor


if __name__ == '__main__':

    fit = Executor('chrome').fit

    def new():
        return controllerNN([17, 8, 8, 6], activation='sigmoid')

    best = new()
    while not fit(best):
        best = new()

    for gen in range(50):
        pop = [best] + [best.mutate() for _ in range(4)] + [new()]
        scores = list(map(fit, pop))
        print('gen %s :' % gen, scores)
        best = pop[np.argsort(scores)[-1]]

    print(scores)
