#!/usr/bin/env python3

from time import sleep
import RPi.GPIO as io

io.setmode(io.BCM)

# Button wired from 3V3 to Pin.  Default state = True.
io.setup(24, io.IN, pull_up_down=io.PUD_DOWN)

# Button wired from Pin to GND.  Default state = False.
io.setup(17, io.IN, pull_up_down=io.PUD_UP)


def callback(channel):
    sleep(0.1)
    status = io.input(24)
    channel = str(channel)
    print("Falling edge detected on " + channel)
    print("Button state is " + str(status))


io.add_event_detect(24, io.FALLING, callback=callback, bouncetime=300)

while True:
    try:
        print("Waiting on button")
        io.wait_for_edge(17, io.RISING, bouncetime=300)
        print("Button press detected")
    except KeyboardInterrupt:
        io.cleanup()
