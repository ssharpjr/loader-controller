#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from time import sleep

a = 0  # Reset iteration
c = 0  # Reset counter

while a < 4:  # Create an exit condition
    print("c = " + str(c))
    # Check the sensor every 10 seconds
    if c == 10:
        print("Checking Sensor")
        a = a + 1

    # Check the API every 5 minutes
    if c == 20:
        print("Checking API")
        a = a + 1
        c = 0

    c = c + 1
    sleep(1)

print("a = " + str(a))
