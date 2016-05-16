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
		lock_file(lockfilename, port)
		yield myserver
	finally:
		logging.debug('Shutting down server...')
		myserver.shutdown()
		free_lock_file(lockfilename)


def read_lock_file(lockfilename):
	"""Read and return the running server process pid"""
	lockfile = open(lockfilename, 'r+')
	server_pid, server_port = lockfile.read().split()
	lockfile.close()
	return (server_pid, server_port)


def check_running(lockfilename, print_info=False):
	"""Read from the server lockfile to see if the server is already running"""
	try:
		server_pid, server_port = read_lock_file(lockfilename)
		status = 'Server running: '
		info = 'process {} on port {}'.format(server_pid, server_port)
	except IOError:
		server_pid = None
		status = 'Server not running'
		info = ''

	msg = '{}{}'.format(status, info)

	if print_info:
		print msg
		logging.debug(msg)

	if server_pid:
		sys.exit()


def shutdown_catalytic_server(lockfilename):
	"""Kill the running server process and exit gracefully to allow removing the lockfile"""
	try:
		server_pid, server_port = read_lock_file(lockfilename)
	except IOError:
		server_pid = None

	if not server_pid:
		logging.error("Cannot shutdown server. It's not running!")
		sys.exit()

	os.kill(int(server_pid), signal.SIGTERM)
	sys.exit()


def sig_exit(sig, stack):
	sys.exit()


def lock_file(lockfilename, port):
	"""Create a file with the running server process pid."""
	server_pid = os.getpid()
	lockfile = open(lockfilename, 'w+')
	lockfile.write('{}\n{}\n'.format(str(server_pid), str(port)))


def free_lock_file(lockfilename=None):
	if lockfilename:
		os.remove(lockfilename)


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'usage: server_driver {start|shutdown|status}'
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
	elif command == 'status':
		check_running(lockfilename, print_info=True)
