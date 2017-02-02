#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP
import RPi.GPIO as IO  # For standard GPIO methods.


###############################################################################
# GPIO Setup
###############################################################################
rst_btn = 18  # INPUT - Manually restart the program.
ir_pin  = 23  # INPUT - Reads the IR sensor state.
ssr_pin = 24  # OUTPUT - Turns on the Solid State Relay.

IO.setmode(IO.BCM)
IO.setup(ssr_pin, IO.OUT, initial=0)

# Wire IR sensor from PIN to GND. Default state = False.
# The edge will RISE when a signal is present.
IO.setup(ir_pin, IO.IN, pull_up_down=IO.PUD_UP)

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
    # TODO: Use dict()
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

