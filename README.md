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

The test_busy script was used to launch 100 client drivers in the
background. This was used for testing response speed for the server.

```
11:40 PM bdecoate:~/catalytic$ ./server_driver.py start &
[1] 11341
11:42 PM bdecoate:~/catalytic$ time ./test_busy.sh 

real    0m3.337s
user    0m2.307s
sys 0m0.562s
```

# Compiling with Cython
A Cython version of the `serverutils.py` file has been included in `serverutils.pyx`.
With Cython installed, use `setup.py build_ext --inplace` to compile the server
utility functions.

The following tests sent these commands to the server:
```
{'factor': 75757575}
{'palindrome': 'was it a cat i saw'}
{'fibonacci': 121212}
{'factor': 757575}
```

The test_busy script here was used to launch 10 client drivers with these
more computationally intense requests.

Previous server version:
```
07:50 AM bdecoate:~/catalytic$ time ./test_busy.sh 
real    0m24.059s
user    0m0.283s
sys 0m0.060s
```

After optimization and Cython compilation:
```
07:51 AM bdecoate:~/catalytic$ time ./test_busy.sh 
real    0m0.059s
user    0m0.235s
sys 0m0.076s
```

A speedup from 24.059s to 0.059s
