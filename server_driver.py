#!/usr/bin/python
import contextlib

from catalyticserver import CatalyticServer


@contextlib.contextmanager
def launch_catalytic_server(host=None, port=None):
	if not host or not port:
		raise ValueError('Server requires host and port')

	myserver = CatalyticServer(host, port)
	myserver.accept_connection()

	try:
		yield myserver
	finally:
		myserver.shutdown()
	return

host = 'localhost'
port = 9500
print 'launching server...'
with launch_catalytic_server(host, port):
	print 'shutting down server'
