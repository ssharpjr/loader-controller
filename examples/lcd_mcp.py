#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Initialize the LCD.

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP
import RPi.GPIO as io  # For standard GPIO methods.

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

