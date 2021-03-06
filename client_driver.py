#!/usr/bin/python

from catalyticclient import CatalyticClient

host = 'localhost'
port = 9500

#  client 1 -- send the factor command
client = CatalyticClient(host, port)
client.connect_to_server()
json = {'factor': 75757575}
client.send(json)
response = client.receive()
client.close()


#  client 2 -- send the palindrome command
client = CatalyticClient(host, port)
client.connect_to_server()
json = {'palindrome': 'was it a cat i saw'}
client.send(json)
response = client.receive()
client.close()


#  client 3 -- send the fibonacci command
client = CatalyticClient(host, port)
client.connect_to_server()
json = {'fibonacci': 121212}
client.send(json)
response = client.receive()
client.close()

#  client 4 -- send the factor command
client = CatalyticClient(host, port)
client.connect_to_server()
json = {'factor': 757575}
client.send(json)
response = client.receive()
client.close()
