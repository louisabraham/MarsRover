#!/usr/bin/env python3 -i

"""
A server to which you send pickled controllers
and that returns their fitness
"""
import argparse

from pickle import loads, dumps

import http.server
import socketserver

from executor import Executor


class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        c = loads(eval(self.headers['controller']))
        ans = dumps(executor.fit(c))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(ans)

parser = argparse.ArgumentParser(description='executor to handle fit requests')
parser.add_argument('port', metavar='port', type=int, nargs='?',
                    default='5555', help='port (default: 5555)')
args = parser.parse_args()

executor = Executor()

httpd = socketserver.TCPServer(("", args.port), Handler)
print("serving at port", args.port)
httpd.serve_forever()
