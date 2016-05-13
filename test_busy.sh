#!/bin/bash
for i in $(seq 10)
do
    ./client_driver.py &
done
wait
