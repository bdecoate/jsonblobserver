#!/usr/bin/python

from catalyticclient import CatalyticClient

host = 'localhost'
port = 9500
client = CatalyticClient(host, port)
client.connect_to_server()
json = {'factor': 75}
print 'sent:', json
client.send(json)
print 'received:', client.receive()
client.close()
