#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import sys
import os
from time import sleep

import RPi.GPIO as IO


# GPIO Setup
btn_pin = 23  # INPUT - Reads the loader plug button.
ssr_pin = 24  # OUTPUT - Turns on the Solid State Relay.

IO.setmode(IO.BCM)
IO.setup(ssr_pin, IO.OUT, initial=0)

# Wire button from PIN to GND.  Default state = False.
# The edge will FALL when pressed.
IO.setup(btn_pin, IO.IN, pull_up_down=IO.PUD_UP)


###############################################################################
def wait_for_button():
    # Wait for button to be released again (btn == 1).
    btn = IO.input(btn_pin)
    while not btn:
        btn = IO.input(btn_pin)
        print("\nButton state: " + str(btn) + " (Button is pressed)")
        sleep(1)

    btn = IO.input(btn_pin)
    print("\nButton state: " + str(btn) + " (Button is released)")
    restart_program()  # Restart the program.


def btn_cb(channel):
    sleep(0.1)
    wait_for_button()


###############################################################################
# Interrupts
# If the button is closed, stop everything until it opens.
IO.add_event_detect(btn_pin, IO.BOTH, callback=btn_cb, bouncetime=300)
###############################################################################


def main():
    print("\nLoader Controller")
    wo_scan = input("Scan Work Order: ")
    print("\nWork Order #" + wo_scan)
    print()


def restart_program():
    print("\nRestarting program")
    # sleep(1)
    IO.cleanup()
    os.execv(__file__, sys.argv)


def run():
    while True:
        try:
            main()
        except:
            IO.cleanup()
            sys.exit()

if __name__ == '__main__':
    run()
