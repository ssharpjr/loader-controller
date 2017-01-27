#!/usr/bin/env python3
from time import sleep

print("Counting loop")

c = 0

while True:
    print("counter: " + str(c))
    c = c + 1
    sleep(.5)
    if c % 10 == 0:
        print("counter hit 10")
    if c % 30 == 0:
        print("counter hit 30")
        print("restarting counter")
        c = 0

