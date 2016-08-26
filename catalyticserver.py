import json
import logging
import threading
import socket

from jsonsocket import JSONBlobSocket
from serverutils import process_request


logging.basicConfig(
	filename='server.log',
	level=logging.DEBUG,
	format='%(asctime)s %(message)s',
	datefmt='%m/%d/%Y %I:%M:%S %p'
)
server_logger = logging.getLogger('serverlog')


class CatalyticServer(JSONBlobSocket):
	def __init__(self, host='127.0.0.1', port=9500):
		super(CatalyticServer, self).__init__(host, port, logger=server_logger)
		try:
			self.sock.bind((self.host, self.port))
			self.listening = True
		except socket.error as msg:
			self.error('Cannot bind socket: %s' % msg)
			self.listening = False

	def accept_connection(self):
		"""Loop forever accepting data on the socket

		Spawn a Thread to handle each incoming connection.
		"""
		try:
			while self.listening:
				self.sock.listen(1)
				conn, addr = self.sock.accept()
				self._threaded_connection(conn)
		except KeyboardInterrupt:
			self.listening = False

	def _threaded_connection(self, conn):
		connection = ConnectionThread(conn, self.logger)
		connection.start()

	def shutdown(self):
		if self.sock:
			self.sock.close()


class ConnectionThread(JSONBlobSocket, threading.Thread):
	def __init__(self, sock, logger):
		threading.Thread.__init__(self)
		self.sock = sock
		self.conn = sock
		self.logger = logger

	def run(self):
		"""Read data accepted from the connection.

		Parse the JSON Blob and execute the desired command.
		Send the result of the command.
		Close the connection when completed.
		"""
		data = self.receive()
		json_data = json.loads(data)
		result = process_request(json_data)
		self.send(result)
		self.close()
