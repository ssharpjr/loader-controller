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
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################


import os
import sys
import requests
from time import sleep
import json

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP
import RPi.GPIO as IO  # For standard GPIO methods.


# Variables
DEBUG = True
api_url = 'http://10.130.0.42'  # Web API URL

# GPIO Setup
rst_btn = 18  # INPUT - Manually restart the program.
ir_pin = 23  # INPUT - Reads the IR sensor state.
ssr_pin = 24  # OUTPUT - Turns on the Solid State Relay.

IO.setmode(IO.BCM)
IO.setup(ssr_pin, IO.OUT, initial=0)

# Wire IR sensor from PIN to GND. Default state = False.
# The edge will RISE when a signal is present.
# IO.setup(ir_pin, IO.IN, pull_up_down=IO.PUD_UP)

# The Banner sensor sends a voltage signal so pull down.
IO.setup(ir_pin, IO.IN, pull_up_down=IO.PUD_DOWN)

# Wire the restart button from PIN to 3V3.  Default state = True.
# The edge will FALL when pressed.
IO.setup(rst_btn, IO.IN, pull_up_down=IO.PUD_DOWN)


###############################################################################
# Setup the LCD and MCP.
###############################################################################
# Define the MCP pins connected to the LCD.
# Note: These are MCP pins, not RPI pins.
lcd_rs = 0
lcd_en = 1
lcd_d4 = 2
lcd_d5 = 3
lcd_d6 = 4
lcd_d7 = 5
lcd_red = 6
lcd_green = 7
lcd_blue = 8
lcd_columns = 20
lcd_rows = 4

# Initialize MCP23017 device using its default 0x20 I2C address.
gpio = MCP.MCP23017()

# Initialize the LCD using the pins.
lcd = LCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                              lcd_columns, lcd_rows, lcd_red, lcd_green,
                              lcd_blue, gpio=gpio)
###############################################################################


def lcd_ctrl(msg, color, clear=True):
    # Send instructions to the LCD.
    # Colors are Red, Green, Blue values.
    # all zeros equals off, all ones equals white
    if clear:
        lcd.clear()

    colors = {
        'red': (1.0, 0.0, 0.0),
        'green': (0.0, 1.0, 0.0),
        'blue': (0.0, 0.0, 1.0),
        'white': (1.0, 1.0, 1.0),
        'off': (0.0, 0.0, 0.0)
        }

    c = colors.get(color)
    lcd.set_color(*c)
    lcd.message(msg)


def get_press_id():
    # Get PRESS_ID from /boot/PRESS_ID file
    # Close the program if no PRESS_ID is found
    press_id_file = "/boot/PRESS_ID"
    try:
        with open(press_id_file) as f:
            PRESS_ID = f.read().replace('\n', '')
            if len(PRESS_ID) >= 3:
                return PRESS_ID
            else:
                raise ValueError("PRESS_ID is Not Assigned!\nExiting")
                sys.exit()
    except IOError:
        print(press_id_file + " Not Found!\nExiting")
        sys.exit()
    except BaseException as e:
        print(e)
        sys.exit()


def network_fail():
    if DEBUG:
        print("Failed to get data from API")
        print("System will restart in 10 seconds.")
    if lcd:
        lcd_ctrl("NETWORK FAILURE\nIf this persists\ncontact TPI IT Dept.\n \
             Restarting...", 'red')
    sleep(5)
    run_or_exit_program('run')


def get_wo_scan():
    if lcd:
        lcd_ctrl("SCAN\n\nWORKORDER NUMBER", 'white')
    # wo_scan = '9934386'  # Should be 9934386 for test.
    wo_scan = input("Scan Workorder: ")
    # wo_scan = sys.stdin.readline().rstrip()
    return wo_scan


def wo_api_request(wo_id):
    # Notify user of potential pause
    if lcd:
        lcd_ctrl("GETTING\nWORKORDER\nINFORMATION...", 'blue')

    url = api_url + '/wo/' + wo_id
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

    try:
        if data['error']:
            if lcd:
                lcd_ctrl("INVALID WORKORDER!", 'red')
            if DEBUG:
                print("Invalid Workorder!  (data = error)")
            sleep(2)  # Pause so the user can read the error.
            run_or_exit_program('run')
    except:
        pass
    try:
        press_from_api_wo = data['press']
        rmat_from_api_wo = data['rmat']
        return press_from_api_wo, rmat_from_api_wo
    except:
        pass


def serial_api_request(sn):
    # Notify user of the potential pause
    if lcd:
        lcd_ctrl("GETTING\nRAW MATERIAL\nSERIAL NUMBER\nINFORMATION...",
                 'blue')

    url = api_url + '/serial/' + sn
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

    try:
        if data['error']:
            if lcd:
                lcd_ctrl("INVALID SERIAL\nNUMBER!", 'red')
            if DEBUG:
                print("Invalid Serial Number! (data = error)")
            sleep(2)  # Pause so the user can read the error.
            run_or_exit_program('run')
    except:
        pass
    try:
        rmat_from_api = data['itemno']
    except:
        pass
    return rmat_from_api


def get_rmat_scan():
    # Get the Raw Material Serial Number.
    # Check for the "S" qualifier.
    # Strip the qualifier is present and return the serial number.
    if lcd:
        lcd_ctrl("SCAN\nRAW MATERIAL\nSERIAL NUMBER", 'white')
    rmat_scan = str(input("Scan Raw Material Serial Number: "))
    if not rmat_scan.startswith('S'):
        if lcd:
            lcd_ctrl("NOT A VALID\nSERIAL NUMBER!", 'red')
        if DEBUG:
            print("Not a Serial Number! (missing \"S\" qualifier)")
        sleep(2)  # Pause so the user can read the error.
        run_or_exit_program('run')
    rmat_scan = rmat_scan[1:]  # Strip off the "S" Qualifier.
    return rmat_scan


def wo_monitor(PRESS_ID, wo_id_from_wo):
    # Check if the workorder number changes (RT workorder unloaded).
    if DEBUG:
        print("Checking loaded workorder")
    url = api_url + '/press/' + PRESS_ID
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

#    if data['error']:
#        lcd_ctrl("WORKORDER CHANGED!\n\nRESTARTING", 'red')
#        if DEBUG:
#            print("Workorder changed! (data = error)")
#        sleep(2)  # Pause so the user can read the error.
#        run_or_exit_program('run')
#
    try:
        press_id_from_api = data['press_id']
        wo_id_from_api = data['wo_id']
        itemno_from_api = data['itemno']
        descrip_from_api = data['descrip']
        itemno_mat_from_api = data['itemno_mat']
        descrip_mat_from_api = data['descrip_mat']
        if DEBUG:
            print("WO from API: " + wo_id_from_api)
    except:
        if DEBUG:
            print("\nAPI Data incomplete")
            print(press_id_from_api)
            print(wo_id_from_api)
            print(itemno_from_api)
            print(descrip_from_api)
            print(itemno_mat_from_api)
            print(descrip_mat_from_api)
            print("\n")

    if wo_id_from_wo != wo_id_from_api:
        if DEBUG:
            print("Workorders do not match.  Restarting")
        run_or_exit_program('run')
    else:
        if DEBUG:
            print("WO looks good, restarting run_mode() loop")


def sensor_monitor():
    # Check to see if the IR beam is broken (0).
    # A broken beam means there is a pallet present.
    if DEBUG == 2:
        print("sensor_monitor() running")
    if IO.input(ir_pin) == 1:
        if DEBUG:
            print("Sensor detected.  Pallet moved")
        if lcd:
            lcd_ctrl("NO PALLET DETECTED\n\nRESTARTING", 'red')
            sleep(2)
        run_or_exit_program('run')
    return


def sensor_startup_check():
    # Check the pallet sensor on startup.
    # Keep checking until it is present.
    if DEBUG:
        print("Checking Pallet Sensor")
    while IO.input(ir_pin) == 1:
        # if IO.input(ir_pin) == 1:
        if DEBUG == 2:
            print("No pallet detected.")
        if lcd:
            lcd_ctrl("NO PALLET DETECTED!\n\nCHECKING AGAIN\nIN 10 SECS",
                     'red')
        sleep(10)
    if lcd:
        lcd_ctrl("PALLET DETECTED\n\nCONTINUING", 'white')
        sleep(2)


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
    if lcd:
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
# def beam_cb(channel):
#     if DEBUG:
#         print("beam_cb() callback called")
#     sleep(0.1)
#     stop_loader()
#     check_outlet_beam()


# def rst_btn_cb(channel):
#     if DEBUG:
#         print("rst_btn_cb() callback called")
#     sleep(0.1)
#     stop_loader()
#     lcd_ctrl("RESETTING\nLOADER\nCONTROLLER", 'white')
#     sleep(1)
#     restart_program()


def run_mode(PRESS_ID, wo_id_from_wo):
    # Run a timed loop, checking the IR sensor and API
    if DEBUG == 2:
        print("run_mode() running")
    c = 0  # Reset counter
    while True:
        if DEBUG == 2:
            print("Counter: " + str(c))
        c = c + 1
        sleep(1)
        if c % 10 == 0:  # Check the sensor every 10 seconds
            if DEBUG == 2:
                print("Counter hit 10")
            sensor_monitor()
        if c % 300 == 0:  # Check the API every 5 minutes
            if DEBUG == 2:
                print("Counter hit 60")
            wo_monitor(PRESS_ID, wo_id_from_wo)
            if DEBUG:
                print("Resetting run_mode() counter")
            c = 0  # Reset counter


###############################################################################
# Interrupts
# If the reset button is pressed, restart the program
# IO.add_event_detect(rst_btn, IO.RISING, callback=rst_btn_cb, bouncetime=300)
###############################################################################


###############################################################################
# Main
###############################################################################

def main():
    # Get the PRESS_ID before doing anything else
    PRESS_ID = get_press_id()

    print("\nStarting Loader Controller Program")
    print("For Press " + PRESS_ID)
    if lcd:
        lcd_msg = "LOADER CONTROLLER\n\n\nPRESS " + PRESS_ID
        lcd_ctrl(lcd_msg, 'white')
    sleep(2)

    # Check if the Pallet Sensor is open (a Pallet is present).
    sensor_startup_check()

    # Request the Workorder Number (ID) Barcode.
    wo_id_from_wo = get_wo_scan()
    if DEBUG:
        print("Scanned Work Order: " + wo_id_from_wo)

    # Request Press Number and Raw Material Item Number from the API.
    if DEBUG:
        print("Requesting data from API")

    try:
        press_from_api_wo, rmat_from_api_wo = wo_api_request(wo_id_from_wo)
    except:
        network_fail()

    if DEBUG:
        print("Press Number from API: " + press_from_api_wo)
        print("RM Item Number from API: " + rmat_from_api_wo)

    # Verify the Press Number.
    if DEBUG:
        print("Checking if workorder is currently running on this press...")
    if press_from_api_wo == PRESS_ID:
        if DEBUG:
            print("Match.  Workorder: " + wo_id_from_wo +
                  " is running on Press #" + PRESS_ID)
            print("Good Workorder.  Continuing...")
    else:
        if lcd:
            lcd_ctrl("INCORRECT\nWORKORDER!", 'red')
        if DEBUG:
            print("Incorrect Workorder!")
            print("This Workorder is for press: " + press_from_api_wo)
        sleep(2)  # Pause so the user can see the error.
        run_or_exit_program('run')

    # Scan the Raw Material Serial Number Barcode.
    serial_from_label = get_rmat_scan()
    if DEBUG:
        print("Serial Number from Label: " + serial_from_label)

    # Request Raw Material Item Number from the API.
    rmat_from_api_inv = serial_api_request(serial_from_label)
    if DEBUG:
        print("RM Item Number from API: " + rmat_from_api_inv)

    # Verify the Raw Material Item Number.
    if DEBUG:
        print("Checking if raw material matches this workorder...")
    if rmat_from_api_wo == rmat_from_api_inv:
        if DEBUG:
            print("Material matches workorder.  Continuing...")
            print("Starting the Loader!")

        start_loader()  # Looks good, turn on the loader.
        if lcd:
            lcd_msg = "PRESS: " + PRESS_ID + "\nWORKORDER: " + wo_id_from_wo +\
                      "\n\nLOADER RUNNING"
            lcd_ctrl(lcd_msg, 'green')
        run_mode(PRESS_ID, wo_id_from_wo)   # Start the monitors
    else:
        if DEBUG:
            print("Invalid Material!")
        if lcd:
            lcd_ctrl("INCORRECT\nMATERIAL!", 'red')
        sleep(2)  # Pause so the user can see the error.
        run_or_exit_program('run')


def run():
    while True:
        try:
            main()
        except KeyboardInterrupt:
            run_or_exit_program('exit')
        except BaseException as e:
            print(e)
            run_or_exit_program('exit')

if __name__ == '__main__':
    run()
