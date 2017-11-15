from pickle import loads, dumps
import urllib.request
import urllib.error, http.client
from multiprocessing.pool import ThreadPool
import subprocess
from time import sleep

"""
client code of rest.py
offers the same fit function as executor.Executor
"""


class RemoteExecutor():

    def __init__(self, address='http://localhost:5555', timeout=3):
        self.address = address
        while True:
            try:
                urllib.request.urlopen(self.address)
            except Exception as e:
                if timeout:
                    sleep(1)
                    timeout -= 1
                else:
                    raise e
            else:
                break

    def fit(self, controller):
        # print('submit task to', self.address)
        req = urllib.request.Request(self.address)
        req.add_header('controller', str(dumps(controller)))
        resp = urllib.request.urlopen(req)
        # print('finish task', self.address)
        return loads(resp.read())


SCRIPT = '/users/eleves-b/2015/louis.abraham/MarsRover/rest.py'
PYTHON = '/usr/local/anaconda3/bin/python3'


class PoolManager():

    def __init__(self, n, script=SCRIPT, python=PYTHON):
        command = ['srun', '-n%s' % n, '--ntasks-per-node=1', 'bash',
                   '-c', '/bin/hostname; %s %s' % (python, script)]
        self.p = subprocess.Popen(command, stdout=subprocess.PIPE)
        self.addresses = ['http://%s:5555' %
                          self.p.stdout.readline().decode()[:-1] for _ in range(n)]
        with ThreadPool(n) as p:
            self.pool = p.map(RemoteExecutor, self.addresses)
        print('Pool of size %s created' % n)

    @staticmethod
    def aux_map_fit(executor, controller):
        return executor.fit(controller)

    def map_fit(self, l):
        ans = []
        while l:
            batch = list(zip(self.pool, l))
            with ThreadPool(len(batch)) as p:
                ans += p.starmap(self.aux_map_fit, batch)
            l = l[len(self.pool):]
        print(ans)
        return ans
