#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test the Powertail Switch II

import sys
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Set pin 23 as a 3V3 output to trigger the PTS
pts = 23
GPIO.setup(pts, GPIO.OUT, initial=0)


# Set pin 24 as an input to read the LED state of the PTS
pts_led = 24
GPIO.setup(pts_led, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    try:
        GPIO.output(pts, 1)
        # print("On")
        if GPIO.input(pts_led):
            print("LED ON")
        else:
            print("LED OFF")

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
    except:
        GPIO.cleanup()
        sys.exit()

