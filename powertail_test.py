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

print("Controlling the Powertail Switch II")

print("Turning on the PTS")
GPIO.output(pts, 1)
print("PTS ON")
sleep(1)

print("\nReading the PTS LED State")
if GPIO.input(pts_led):
    print("PTS LED is ON")
else:
    print("PTS LED is OFF or not registering")
sleep(5)

print("\nTurning off the PTS")
GPIO.output(pts, 0)
print("PTS OFF")
sleep(1)

print("\nReading the PTS LED State")
if GPIO.input(pts_led):
    print("PTS LED is ON")
else:
    print("PTS is OFF or not registering!")
sleep(5)




print("\nCleaning up and exiting")
GPIO.cleanup()

# while True:
#    try:
#        GPIO.output(pts, 1)
#        print("On")
#        sleep(1)
#        GPIO.output(pts, 0)
#        print("Off")
#        sleep(1)
#    except KeyboardInterrupt:
#        GPIO.cleanup()
#        sys.exit()
#    except:
#        GPIO.cleanup()
#        sys.exit()

