import socket
import json
import struct


class JSONBlobSocket(object):
	def __init__(self, host='127.0.0.1', port=9500, logger=None):
		self.port = port
		self.host = host
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.logger = logger

	def log(self, message):
		if self.logger:
			self.logger.debug(message)

	def send(self, json_data):
		if not self.conn:
			return

		json_str = json.dumps(json_data)
		packed_data = struct.pack('%ds' % len(json_str), json_str)
		header_data = struct.pack('I', len(json_str))
		self._send(header_data)
		self._send(packed_data)
		self.log('Sent %d bytes: %s' % (len(json_str), json_str))

	def _send(self, data):
		sent_data = 0
		while sent_data < len(data):
			try:
				sent_data = self.conn.send(data[sent_data:])
			except socket.error as msg:
				print 'error sending:', msg
				return

	def receive(self):
		header_data = self._read_header()
		json_data = self._receive(header_data)
		self.log('Received %d bytes: %s' % (header_data, json_data))
		return json_data

	def _receive(self, json_len):
		recv_data = ''
		while len(recv_data) < json_len:
			buffer_data = self.conn.recv(json_len - len(recv_data))
			recv_data += buffer_data
		return recv_data

	def _read_header(self):
		header_data = self._receive(4)
		return struct.unpack('I', header_data)[0]

	def close(self):
		self.sock.close()