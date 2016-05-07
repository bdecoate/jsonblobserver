import json
import logging
import threading

from jsonsocket import JSONBlobSocket
from serverutils import process_request


logging.basicConfig(filename='server.log', level=logging.ERROR,
	format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
server_logger = logging.getLogger('serverlog')


class CatalyticServer(JSONBlobSocket):
	def __init__(self, host='127.0.0.1', port=9500):
		super(CatalyticServer, self).__init__(host, port, logger=server_logger)
		self.sock.bind((self.host, self.port))
		self.listening = True

	def accept_connection(self):
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
		data = self.receive()
		json_data = json.loads(data)
		result = process_request(json_data)
		self.send(result)
		self.close()
