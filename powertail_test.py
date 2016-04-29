#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test the Powertail Switch II

import sys
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Set pin 23 as a 3V3 output to trigger the PTS2
pts = 23
GPIO.setup(pts, GPIO.OUT, initial=0)

print("Controlling the Powertail Switch II")
while True:
    try:
        GPIO.output(pts, 1)
        print("On")
        sleep(1)
        GPIO.output(pts, 0)
        print("Off")
        sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
    except:
        GPIO.cleanup()
        sys.exit()

