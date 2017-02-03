#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# The MIT License (MIT)
#
# Copyright (c) 2016 Stacey Sharp (github.com/ssharpjr)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

# TODO: Pull PRESS_ID from /boot/pressid.txt. This will allow for better
#       replication to other presses.
# TODO: Implement logging

import os
import sys

from iqapi import *
from lcdmcp import *


# CONSTANTS
DEBUG = True
PRESS_ID = '136'  # This does not change!


def network_fail():
    if DEBUG:
        print("Failed to get data from API")
        print("System will restart in 5 seconds.")
    if lcd_ctrl:
        lcd_ctrl("NETWORK FAILURE\nIf this persists\ncontact TPI IT Dept.\nRestarting...", 'red')
    sleep(5)
    run_or_exit_program('run')


def get_wo_scan():
    if lcd_ctrl:
        lcd_ctrl("SCAN\n\nWORKORDER NUMBER", 'white')
    wo_scan = input("Scan Workorder: ")
    return wo_scan


def get_rmat_scan():
    # Get the Raw Material Serial Number.
    # Check for the "S" qualifier.
    # Strip the qualifier if present and return the serial number.
    if lcd_ctrl:
        lcd_ctrl("SCAN\nRAW MATERIAL\nSERIAL NUMBER", 'white')
    rmat_scan = ''
    if DEBUG:
        rmat_scan = str(input("Scan Raw Material Serial Number: "))
    if not rmat_scan.startswith('S'):
        if lcd_ctrl:
            lcd_ctrl("NOT A VALID\nSERIAL NUMBER!", 'red')
        if DEBUG:
            print("Not a Serial Number! (missing \"S\" qualifier)")
        sleep(2)  # Pause so the user can read the error.
        run_or_exit_program('run')
    rmat_scan = rmat_scan[1:]  # Strip off the "S" Qualifier.
    return rmat_scan


def get_wo_id_from_api(press_id):
    # Get API data
    wo_id_from_api = wo_id_api_request(press_id)
    return wo_id_from_api


def compare_press_id(PRESS_ID):
    pass


def compare_wo_id(wo_scan, wo_id_from_api, PRESS_ID):
    press_id = PRESS_ID

    # Notify user of potential pause
    if lcd_ctrl:
        lcd_ctrl("GETTING\nWORK ORDER\nINFORMATION...", 'blue')
    wo_id_from_wo = get_wo_scan()
    wo_id_from_api = get_wo_id_from_api(press_id)


def sensor_monitor():
    # Check to see if the IR beam is broken (0).
    # A broken beam means there is pallet present; good to run.
    if IO.input(ir_pin) == 1:
        if DEBUG:
            print("Sensor detected.  Pallet moved")
        run_or_exit_program('run')


def wo_monitor():
    wo_id_from_api = press_api_request(PRESS_ID, wo_id_from_wo)
    if wo_id_from_api != wo_id_from_wo:
        if DEBUG:
            print("Work order changed! (work orders do not match)")
        lcd_ctrl("WORK ORDER\nCHANGED\n\nRESTARTING", 'red')
        run_or_exit_program('run')


def start_loader():
    if DEBUG:
        print("\nEnergizing Loader")
    sleep(0.5)
    IO.output(ssr_pin, 1)  # Turn on the Solid State Relay.


def stop_loader():
    if DEBUG:
        print("\nDe-energizing Loader")
    sleep(0.5)
    IO.output(ssr_pin, 0)  # Turn off the Solid State Relay.


def restart_program():
    print("\nRestarting program")
    # sleep(1)
    IO.cleanup()
    os.execv(__file__, sys.argv)


def reboot_system():
    lcd.clear()
    lcd_ctrl("REBOOTING SYSTEM\n\nSTANDBY...", 'blue')
    IO.cleanup()
    os.system('sudo reboot')


def run_or_exit_program(status):
    if status == 'run':
       restart_program()
    elif status == 'exit':
        print("\nExiting")
        lcd.set_color(0, 0, 0)  # Turn off backlight
        lcd.clear()
        IO.cleanup()
        sys.exit()


# Interrupt Callback function
def beam_cb(channel):
    if DEBUG:
        print("beam_cb() callback called")
    sleep(0.1)
    stop_loader()
    check_outlet_beam()


def rst_btn_cb(channel):
    if DEBUG:
        print("rst_btn_cb() callback called")
    sleep(0.1)
    stop_loader()
    lcd_ctrl("RESETTING\nLOADER\nCONTROLLER", 'white')
    sleep(1)
    restart_program()


def run_mode():
    # Run a timed loop, checking the IR sensor and API
    if DEBUG:
        print("run_mode() running")

    c = 0  # Reset counter
    while True:
        c = c + 1
        sleep(1)
        if c % 10 == 0:  # Check the sensor every 10 seconds
            sensor_monitor()
        if c % 300 == 0:  # Check the API every 5 minutes
            wo_monitor()
            c = 0  # Reset counter when 300 is hit


###############################################################################
# Interrupts
# If the reset button is pressed, restart the program
# IO.add_event_detect(rst_btn, IO.RISING, callback=rst_btn_cb, bouncetime=300)
###############################################################################


###############################################################################
# Main
###############################################################################

def main():
    # Begin
    print()
    print("Starting Loader Controller Program")
    print("For Press " + PRESS_ID)
    if lcd_ctrl:
        lcd_msg ="LOADER CONTROLLER\n\n\nPRESS " + PRESS_ID
        lcd_ctrl(lcd_msg, 'white')
    sleep(1)


    # TODO: Complete Process Flow.

    # Scan the Workorder Number (ID) Barcode.
    get_wo_id_from_scan()

    # Request Press info from API using PRESS_ID.
    get_press_api_data(PRESS_ID)

    # Verify the Press Number using PRESS_ID.
    compare_press_id(press_id)

    # Verify the Work Order Number using PRESS_ID, wo_id_from_scan.
    compare_wo_id(PRESS_ID, wo_id_from_scan)

    # Scan the Raw Material Serial Number Barcode.
    get_serial_number_from_scan()

    # Request Raw Material Item Number from the API using serial_from_scan.
    get_itemno_mat_from_serial_api(serial_from_scan)

    # Verify the Raw Material Item Number.
    # Using itemno_mat_from_press_api, itemno_mat_from_serial_api
    compare_rmat_itemno(itemno_mat_from_press_api, itemno_mat_from_serial_api)

    # Energize the loader.
    start_loader()

    # Execute run_mode() function.
    run_mode()


def run():
    while True:
        try:
            main()
        except KeyboardInterrupt:
            run_or_exit_program('exit')
        except:
            # stop_loader()
            print("GPIO Cleanup")
            IO.cleanup()


if __name__ == '__main__':
    run()
