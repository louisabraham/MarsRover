from pickle import loads, dumps
import urllib.request

"""
client code of rest.py
offers the same fit function as executor.Executor
"""

class RemoteExecutor():

    def __init__(self, address='http://localhost:5555'):
        self.address = address

    def fit(self, controller):
        req = urllib.request.Request(self.address)
        req.add_header('controller', str(dumps(controller)))
        resp = urllib.request.urlopen(req)
        return loads(resp.read())
