#!/usr/bin/env python

import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()

import time

port = 8080

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", port)
handler.cgi_directories = ["/"]
httpd = server(server_address, handler)

print "Server listening on port %d at %s..." % (port, time.ctime())

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()

print
print "Server closed on port %d at %s." % (port, time.ctime())
