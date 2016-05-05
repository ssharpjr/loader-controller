#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import sys
import os
from time import sleep

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP
import RPi.GPIO as IO  # For standard GPIO methods.


# GPIO Setup
ssr_pin = 23  # OUTPUT - Turns on the Solid State Relay
btn_pin = 24  # INPUT - Reads the outlet cover button

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
    else: 
        lcd.set_color(0.0, 0.0, 0.0)  # Off
    lcd.message(msg)

###############################################################################

def wait_for_button():
    # Wait for button to be released again (btn == 1).
    btn = IO.input(btn_pin)
    while btn == 0:
        sleep(1)
    restart_program()  # Restart the program.


def check_loader():
    btn = IO.input(btn_pin)
    sleep(0.1)
    if btn == 0:  # Button state reversed due to pull down resistor.
        print("\nButton is pressed (No loader connected)")
        lcd_ctrl("NO LOADER PRESENT!", 'red')
        wait_for_button()
    if btn == 1:  # Button state reversed due to pull down resistor.
        print("\nButton is released (Loader connected)")
        lcd_ctrl("LOADER DETECTED", 'green')
        restart_program()  # Restart the program.
    sleep(3)

def break_run():
    sleep(0.1)
    if IO.input(btn_pin) == 0:
        return False
    else:
        return True


def btn_cb(channel):
    break_run()
    check_loader()


###############################################################################
# Interrupts
# If the button is closed, stop everything until it opens.
IO.add_event_detect(btn_pin, IO.FALLING, callback=btn_cb, bouncetime=300)
###############################################################################


def main():
    print("\nLoader Controller")
    lcd_ctrl("SCAN\nWORK ORDER NUMBER", 'white')
    wo_scan = input("Scan Work Order: ")
    print("\nWork Order #" + wo_scan)
    print()


def exit_program():
    # Turn off LCD, cleanup and exit
    lcd.clear()
    lcd.set_backlight(0)
    lcd.enable_display(False)
    IO.cleanup()
    # sys.exit()


def restart_program():
    exit_program()
    os.execv(__file__, sys.argv)


def run():
    while True:
        if not break_run():
            break
        else:
            main()

if __name__ == '__main__':
    run()
