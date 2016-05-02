#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: Setup Loader Controller


import sys
import requests
import time
import json

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP
import RPi.GPIO as io  # For standard GPIO methods.

# CONSTANTS
PRESS_ID = '125'  # Should be 125 for test.  This does not change!

# Variables
DEBUG = True
api_url = 'http://localhost:5000'


###############################################################################
# Setup the LCD and MCP.
###############################################################################
# Define the MCP pins connected to the LCD.
lcd_rs = 0
lcd_en = 1
lcd_d4 = 2
lcd_d5 = 3
lcd_d6 = 4
lcd_d7 = 5
lcd_red = 6
lcd_green = 7
lcd_blue = 8

# Define LCD column and row size for a 20x4 LCD.
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


def get_wo_scan():
    lcd_ctrl("SCAN\nWORKORDER\nNUMBER", white)
    if DEBUG:
        wo_scan = input("Scan Workorder: ")
    else:
        wo_scan = input()  # No console output
    # wo_scan = '9934386'  # Should be 9934386 for test.
    return wo_scan


def wo_api_request(wo_id):
    url = api_url + '/wo/' + wo_id
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    try:
        if data['error']:
            lcd_ctrl("INVALID WORKORDER!", red)
            if DEBUG:
                print("Invalid Workorder!")
            sleep(5)  # Pause so the user can read the error.
            run_or_exit_program('run')
    except:
        pass
    try:
        press_from_wo = data['press']
        rmat_from_wo = data['rmat']
        return press_from_wo, rmat_from_wo
    except:
        pass


def serial_api_request(sn):
    url = api_url + '/serial/' + sn
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    try:
        if data['error']:
            lcd_ctrl("INVALID SERIAL\nNUMBER!", red)
            if DEBUG:
                print("Invalid Serial Number!")
            sleep(5)  # Pause so the user can read the error.
            run_or_exit_program('run')
    except:
        pass
    rmat_from_api = data['itemno']
    return rmat_from_api


def get_rmat_scan():
    lcd_ctrl("SCAN\nRAW MATERIAL\nSERIAL NUMBER", white)
    if DEBUG:
        rmat_scan = str(input("Scan Raw Material Serial Number: "))
    else:
        rmat_scan = str(input())
    # rmat_scan = 'S07234585' for test.
    if not rmat_scan.startswith('S'):
        lcd_ctrl("NOT A VALID\nSERIAL NUMBER!", red)
        if DEBUG:
            print("Not a Serial Number!")
        sleep(5)  # Pause so the user can read the error.
        run_or_exit_program('run')
    rmat_scan = rmat_scan[1:]  # Strip off the "S" Qualifier.
    return rmat_scan


def start_loader():
    # TODO
    # GPIO control for PST.
    input("Loader is running.  Press ENTER to exit test.")
    run_or_exit_program('exit')


def run_or_exit_program(status):
    if status == 'run':
        if DEBUG:
            print("Starting over...")
        run()
    elif status == 'exit':
        if DEBUG:
            print("Exiting")
        sys.exit()


###############################################################################
# Main
###############################################################################

def main():
    lcd_msg ="LOADER\nCONTROLLER\nASSIGNED TO\nPRESS" + PRESS_ID
    lcd_ctrl(lcd_msg, white)
    if DEBUG:
        print("This is Press: " + PRESS_ID)
    sleep(3)
    # Scan the Workorder Number (ID) Barcode.
    wo_id_from_wo = get_wo_scan()

    # Request Press Number and Raw Material Item Number from the API.
    press_from_wo, rmat_from_wo = wo_api_request(wo_id_from_wo)

    # Verify the Press Number.
    if DEBUG:
        print("Checking if workorder is currently running on this press...")
    if press_from_wo == PRESS_ID:
        if DEBUG:
            print("Match.  Workorder #" + wo_id_from_wo +
                  " is running on Press #" + PRESS_ID)
            print("Good Workorder.  Continuing...")
    else:
        lcd_ctrl("INCORRECT\nWORKORDER!", red)
        if DEBUG:
            print("Incorrect Workorder!")
            print("This Workorder is for press: " + press_from_wo)
        sleep(5)  # Pause so the user can see the error.
        run_or_exit_program('run')

    # Scan the Raw Material Serial Number Barcode.
    serial_from_label = get_rmat_scan()

    # Request Raw Material Item Number from the API.
    rmat_from_api = serial_api_request(serial_from_label)

    # Verify the Raw Material Item Number.
    if DEBUG:
        print("Checking if raw material matches this workorder...")
    if rmat_from_wo == rmat_from_api:
        if DEBUG:
            print("Material matches workorder.  Continuing...")
            print("Starting the Loader!")
        # Display Press ID, FG Item Description and RM Description?
        lcd_msg = "Press #" + PRESS_ID
        lcd_ctrl(lcd_msg, green)
        start_loader()
    else:
        print("Invalid Material!")
        run_or_exit_program('run')


def run():
    while True:
        main()


if __name__ == '__main__':
    run()
