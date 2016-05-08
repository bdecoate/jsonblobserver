JSON Blob Server
=====

# Description
A multithreaded server for handling simple JSON Blobs passed on port 9500.

A base socket class is implemented for creating functionality for sending
and receiving JSON Blobs. The server creates a thread to handle processing
new connections accepted. The thread will process and execute the requested
command and send back the result before closing the connection and exiting.

A client class is implemented to test sending messages to the server.

The server driver is the main executable for running the server. The usage
is: `usage: server_driver [start|shutdown]`. The client driver
will create three clients, one for each type of command.

The test_busy script will launch 100 client drivers in the background. This
was used for testing response speed for the server.

# Example Usage

```
11:33 PM bdecoate:~/catalytic$ ./server_driver.py start &
[1] 11251
11:33 PM bdecoate:~/catalytic$ ./client_driver.py 
11:33 PM bdecoate:~/catalytic$ ./server_driver.py shutdown
[1]+  Done                    ./server_driver.py start
```

```
11:33 PM bdecoate:~/catalytic$ cat client.log
05/07/2016 11:33:20 PM Sent 14 bytes: {"factor": 75}
05/07/2016 11:33:20 PM Received 9 bytes: [3, 5, 5]
05/07/2016 11:33:20 PM Sent 36 bytes: {"palindrome": "was it a cat i saw"}
05/07/2016 11:33:20 PM Received 4 bytes: true
05/07/2016 11:33:20 PM Sent 17 bytes: {"fibonacci": 12}
05/07/2016 11:33:20 PM Received 3 bytes: 144
```

```
11:40 PM bdecoate:~/catalytic$ ./server_driver.py start &
[1] 11341
11:42 PM bdecoate:~/catalytic$ time ./test_busy.sh 

real    0m3.337s
user    0m2.307s
sys 0m0.562s
```
