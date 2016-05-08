#!/bin/bash
for i in $(seq 100)
do
    ./client_driver.py &
done
wait
