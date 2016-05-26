#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as IO

IO.setmode(IO.BCM)
IO.setup(18, IO.IN, pull_up_down=IO.PUD_DOWN)

print("Waiting for button press")
try:
    while True:
        IO.wait_for_edge(18, IO.FALLING)
        print("Button pressed")

        for i in range(60):
            if IO.input(18):
                break  # Button was released
            sleep(0.05)  # 20ms

        # if 25 <= i < 58:  # If button released between 1.25s and 3s, close program
        #    print("Closing program")
        #    break

        if not IO.input(18):
            if i >= 59:
                print("Shutting Down")
                break
except KeyboardInterrupt:
    IO.cleanup()
