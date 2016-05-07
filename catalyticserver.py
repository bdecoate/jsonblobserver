import json
import contextlib
import logging
from jsonsocket import JSONBlobSocket

logging.basicConfig(filename='server.log', level=logging.DEBUG,
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
				self.conn, addr = self.sock.accept()
				data = self.receive()
				json_data = json.loads(data)
				self.send(json_data)
				self.conn.close()
		except KeyboardInterrupt:
			self.listening = False

	def shutdown(self):
		if self.sock:
			self.sock.close()


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
