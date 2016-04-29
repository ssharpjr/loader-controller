#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Reads the input from the Powertail Switch II LED.
# The LED has been removed.

import sys
from time import sleep
import RPi.GPIO as io

io.setmode(io.BCM)

# Set pin 23 as the input
pts = 23
io.setup(23, io.IN, pull_up_down=io.PUD_DOWN)

print("Reading PTS State")
if io.input(pts):
    print("PTS is ON")
else:
    print("PTS is OFF")

print("Cleaning up")
io.cleanup()
print("Exiting")

