#!/usr/bin/python
from catalyticserver import launch_catalytic_server

host = 'localhost'
port = 9500
print 'launching server...'
with launch_catalytic_server(host, port):
	print 'shutting down server'
