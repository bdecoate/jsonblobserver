#!/usr/bin/python

from catalyticclient import CatalyticClient

host = 'localhost'
port = 9500

client = CatalyticClient(host, port)
client.connect_to_server()
json = {'factor': 75}
client.send(json)
response = client.receive()
client.close()

client = CatalyticClient(host, port)
client.connect_to_server()
json = {'palindrome': 'was it a cat i saw'}
client.send(json)
response = client.receive()
client.close()

client = CatalyticClient(host, port)
client.connect_to_server()
json = {'fibonacci': 12}
client.send(json)
response = client.receive()
client.close()
