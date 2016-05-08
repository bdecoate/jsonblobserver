#!/usr/bin/python
import contextlib
import logging
import sys
import os
import signal

from catalyticserver import CatalyticServer


@contextlib.contextmanager
def launch_catalytic_server(host=None, port=None, lockfilename=None):
	"""Yield a server instance (if one isn't already running) and terminate on exit"""

	if not host or not port:
		raise ValueError('Server requires host and port')

	check_running(lockfilename)

	try:
		logging.debug('Starting server...')
		myserver = CatalyticServer(host, port)
		signal.signal(signal.SIGTERM, sig_exit)
		lock_file(lockfilename)
		yield myserver
	finally:
		logging.debug('Shutting down server...')
		myserver.shutdown()
		free_lock_file(lockfilename)


def read_lock_file(lockfilename):
	"""Read and return the running server process pid"""
	lockfile = open(lockfilename, 'r+')
	server_pid = int(lockfile.read().strip())
	lockfile.close()
	return server_pid


def check_running(lockfilename):
	"""Read from the server lockfile to see if the server is already running"""
	try:
		server_pid = read_lock_file(lockfilename)
	except IOError:
		server_pid = None

	if server_pid:
		logging.error('Server already running')
		sys.exit()


def shutdown_catalytic_server(lockfilename):
	"""Kill the running server process and exit gracefully to allow removing the lockfile"""
	try:
		server_pid = read_lock_file(lockfilename)
	except IOError:
		server_pid = None

	if not server_pid:
		logging.error("Cannot shutdown server. It's not running!")
		sys.exit()

	os.kill(server_pid, signal.SIGTERM)
	sys.exit()


def sig_exit(sig, stack):
	sys.exit()


def lock_file(lockfilename):
	"""Create a file with the running server process pid."""
	server_pid = os.getpid()
	lockfile = open(lockfilename, 'w+')
	lockfile.write('{}\n'.format(str(server_pid)))


def free_lock_file(lockfilename=None):
	if lockfilename:
		os.remove(lockfilename)


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage: server_driver [start|shutdown]'
		sys.exit()

	lockfilename = '/tmp/catalyticserver.pid'
	host = 'localhost'
	port = 9500

	command = sys.argv[1]
	if command == 'start':
		with launch_catalytic_server(host, port, lockfilename) as myserver:
			myserver.accept_connection()
	elif command == 'shutdown':
		shutdown_catalytic_server(lockfilename)
