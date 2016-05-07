import socket
import logging

from jsonsocket import JSONBlobSocket

logging.basicConfig(filename='client.log', level=logging.DEBUG,
	format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
client_logger = logging.getLogger('clientlog')


class CatalyticClient(JSONBlobSocket):
	def __init__(self, host='127.0.0.1', port=9500):
		super(CatalyticClient, self).__init__(host, port, logger=client_logger)
		self.conn = self.sock

	def connect_to_server(self):
		try:
			self.sock.connect((self.host, self.port))
		except socket.error:
			print "could not connect"
