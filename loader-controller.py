#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: Setup Loader Controller


import os
import sys
import requests
from time import sleep
import json

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP
import RPi.GPIO as IO  # For standard GPIO methods.


# CONSTANTS
DEBUG = True
PRESS_ID = '136'  # Should be 125 for test.  This does not change!


# Variables
api_url = 'http://10.130.2.148'  # Web API URL


# GPIO Setup
btn_pin = 23  # INPUT - Reads the outlet cover button
ssr_pin = 24  # OUTPUT - Turns on the Solid State Relay

IO.setmode(IO.BCM)
IO.setup(ssr_pin, IO.OUT, initial=0)

# Wire button from PIN to GND. Default state = False.
# The edge will FALL when pressed.
IO.setup(btn_pin, IO.IN, pull_up_down=IO.PUD_UP)



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
    color = color
    if clear:
        lcd.clear()
    if color == 'red':
        lcd.set_color(1.0, 0.0, 0.0)  # Red
    elif color == 'green':
        lcd.set_color(0.0, 1.0, 0.0)  # Green
    elif color == 'blue':
        lcd.set_color(0.0, 0.0, 1.0)  # Blue
    elif color == 'white':
        lcd.set_color(1.0, 1.0, 1.0)  # White
    elif color == 'off':
        lcd.set_color(0.0, 0.0, 0.0)  # Off
    else:
        lcd.set_color(0.0, 0.0, 0.0)  # Off
    lcd.message(msg)


def network_fail():
    if DEBUG:
        print("Failed to get data from API")
    lcd_ctrl("NETWORK FAILURE\nIf this persists\ncontact TPI IT Dept.\nRestarting...", 'red')
    sleep(10)
    run_or_exit_program('run')


def get_wo_scan():
    lcd_ctrl("SCAN\n\nWORKORDER NUMBER", 'white')
    # wo_scan = '9934386'  # Should be 9934386 for test.
    wo_scan = input("Scan Workorder: ")
    # wo_scan = sys.stdin.readline().rstrip()
    return wo_scan


def wo_api_request(wo_id):
    # Notify user of potential pause
    lcd_ctrl("GETTING\nWORKORDER\nINFORMATION...", 'blue')

    url = api_url + '/wo/' + wo_id
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

    try:
        if data['error']:
            lcd_ctrl("INVALID WORKORDER!", 'red')
            if DEBUG:
                print("Invalid Workorder!")
            sleep(5)  # Pause so the user can read the error.
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
    lcd_ctrl("GETTING\nRAW MATERIAL\nSERIAL NUMBER\nINFORMATION...", 'blue')

    url = api_url + '/serial/' + sn
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

    try:
        if data['error']:
            lcd_ctrl("INVALID SERIAL\nNUMBER!", 'red')
            if DEBUG:
                print("Invalid Serial Number!")
            sleep(5)  # Pause so the user can read the error.
            run_or_exit_program('run')
    except:
        pass
    try:
        rmat_from_api = data['itemno']
    except:
        pass
    return rmat_from_api


def get_rmat_scan():
    lcd_ctrl("SCAN\nRAW MATERIAL\nSERIAL NUMBER", 'white')
    # rmat_scan = 'S07234585' for test.
    rmat_scan = ''
    if DEBUG:
        rmat_scan = str(input("Scan Raw Material Serial Number: "))
    else:
        rmat_scan = str(input())
    if not rmat_scan.startswith('S'):
        lcd_ctrl("NOT A VALID\nSERIAL NUMBER!", 'red')
        if DEBUG:
            print("Not a Serial Number!")
        sleep(5)  # Pause so the user can read the error.
        run_or_exit_program('run')
    rmat_scan = rmat_scan[1:]  # Strip off the "S" Qualifier.
    return rmat_scan


def wo_monitor(wo_id_from_wo):
    # TODO - API: check first workorder ID
    # Check if the workorder number changes (RT job unloaded).
    wo_id = wo_id_from_wo
    url = api_url + '/wo/' + wo_id
    resp = requests.get(url=url, timeout=10)
    data = json.loads(resp.text)

    wo_id_from_api = data['wo_id']


def start_loader():
    if DEBUG:
        print("\nEnergizing Loader")
    sleep(1)
    IO.output(ssr_pin, 1)  # Turn on the Solid State Relay.


def stop_loader():
    if DEBUG:
        print("\nDe-energizing Loader")
    sleep(1)
    IO.output(ssr_pin, 0)  # Turn off the Solid State Relay.


def restart_program():
    print("\nRestarting program")
    # sleep(1)
    IO.cleanup()
    os.execv(__file__, sys.argv)


def run_or_exit_program(status):
    if status == 'run':
       restart_program()
    elif status == 'exit':
        print("\nExiting")
        stop_loader()
        lcd.set_color(0, 0, 0)  # Turn off backlight
        lcd.clear()
        IO.cleanup()
        sys.exit()


def check_outlet_button():
    btn = IO.input(btn_pin)
    if btn == 0:  # Button is pressed, outlet closed.
        if DEBUG:
            print("\nButton is pressed (Outlet cover closed).")
        lcd_ctrl("LOADER NOT FOUND!\n\nPlease check the\nLoader outlet", 'red')
        wait_for_button()


def wait_for_button():
    # Wait for button to be released again (btn == 1).
    btn = IO.input(btn_pin)
    while not btn:
        btn = IO.input(btn_pin)
        # lcd_ctrl("LOADER NOT FOUND!\n\nPlease check the\nLoader outlet", 'red')
        sleep(3)

    btn = IO.input(btn_pin)
    print("\nButton state: " + str(btn) + " (Button is released)")
    restart_program()  # Restart the program (Break out of the input loop).


# Interrupt Callback function
def btn_cb(channel):
    sleep(0.1)
    stop_loader()
    check_outlet_button()

###############################################################################
# Interrupts
# If the outlet button is closed, stop everything until it opens.
IO.add_event_detect(btn_pin, IO.FALLING, callback=btn_cb, bouncetime=300)
###############################################################################


###############################################################################
# Main
###############################################################################

def main():

    print("Starting Loader Controller Program")
    lcd_msg ="LOADER CONTROLLER\n\n\nPRESS " + PRESS_ID
    lcd_ctrl(lcd_msg, 'white')
    sleep(3)


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
        lcd_ctrl("INCORRECT\nWORKORDER!", 'red')
        if DEBUG:
            print("Incorrect Workorder!")
            print("This Workorder is for press: " + press_from_api_wo)
        sleep(5)  # Pause so the user can see the error.
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

        lcd_msg = "PRESS: " + PRESS_ID + "\n\nWORKORDER: " + wo_id
        lcd_ctrl(lcd_msg, 'green')
        start_loader()  # Looks good, turn on the loader.
        wo_monitor(wo_id_from_wo)  # Watch if the workorder number changes.
    else:
        if DEBUG:
            print("Invalid Material!")
        lcd_ctrl("INCORRECT\nMATERIAL!", 'red')
        sleep(5)  # Pause so the user can see the error.
        run_or_exit_program('run')


def run():
    while True:
        try:
            check_outlet_button()
            main()
        except KeyboardInterrupt:
            run_or_exit_program('exit')


if __name__ == '__main__':
    run()
