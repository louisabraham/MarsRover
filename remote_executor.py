from pickle import loads, dumps
import urllib.request
from multiprocessing.pool import ThreadPool
import subprocess


"""
client code of rest.py
offers the same fit function as executor.Executor
"""


class RemoteExecutor():

    def __init__(self, address='http://localhost:5555'):
        self.address = address
        urllib.request.get(self.address)

    def fit(self, controller):
        req = urllib.request.Request(self.address)
        req.add_header('controller', str(dumps(controller)))
        resp = urllib.request.urlopen(req)
        return loads(resp.read())


SCRIPT = '/users/eleves-b/2015/louis.abraham/MarsRover/rest.py'
PYTHON = '/usr/local/anaconda3/bin/python3'


class PoolManager():

    def __init__(self, n, script=SCRIPT, python=PYTHON):
        command = ['srun', '-n%s' % n, '--ntasks-per-node=1', 'bash',
                   '-c', '/bin/hostname; %s %s' % (python, script)]
        self.p = subprocess.Popen(command, stdout=subprocess.PIPE)
        self.pool = [RemoteExecutor('http://%s:5555' %
                                    self.p.stdout.readline().decode()[:-1]) for _ in range(n)]

    @staticmethod
    def aux_map_fit(executor, controller):
        return executor.fit(controller)

    def map_fit(self, l):
        ans = []
        while l:
            batch = list(zip(self.pool, l))
            with ThreadPool(len(batch)) as p:
                ans += p.starmap(self.aux_map_fit, batch)
        return ans
