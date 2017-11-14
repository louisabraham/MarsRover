import numpy as np

from GNN import controllerNN

from remote_executor import PoolManager


if __name__ == '__main__':

    N = 6

    pm = PoolManager(N)
    fit = pm.pool[0].fit

    def new():
        return controllerNN([17, 8, 8, 6], activation='sigmoid')

    pop = [new() for _ in range(N)]
    scores = pm.map_fit(pop)
    while not any(scores):
        pop = [new() for _ in range(N)]
        scores = pm.map_fit(pop)

    best = pop[np.argsort(scores)[-1]]

    for gen in range(50):
        pop = [best] + [best.mutate() for _ in range(4)] + [new()]
        scores = pm.map_fit(pop)
        print('gen %s :' % gen, scores)
        best = pop[np.argsort(scores)[-1]]

    print(scores)
