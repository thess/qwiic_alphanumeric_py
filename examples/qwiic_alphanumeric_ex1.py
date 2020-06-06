#!/usr/bin/python3

# Basic example of setting digits on a LED segment display.
# This example and library is meant to work with the Sparkfun qwiic_alphanumeric display.
# Author: Ted Hess
# License: Public Domain

import pydevd_pycharm
pydevd_pycharm.settrace('m4800', port=6969, stdoutToServer=True, stderrToServer=True)

import time
import sys

# Import the HT16K33 LED segment module.
import qwiic_alphanumeric as qa

display = qa.QwiicAlphanumeric()

if display.connected == False:
    print("The Qwiic Alphanumeric device isn't connected to the system. Please check your connection", \
          file=sys.stderr)
    exit(1)

# Init and clear Clear the display.
display.begin()

# Can just print a number
display.print(42)
time.sleep(2)

display.print(53.2)
time.sleep(2)

# Or, can print a hexadecimal value
display.print_hex(0xFF23)
time.sleep(2)

# Or, print the time
display.print("12:30")
time.sleep(2)

display.colon = False

# Or, can set individual digits / characters
# Set the first character to '1':
display[0] = "1"
# Set the second character to '2':
display[1] = "2"
# Set the third character to 'A':
display[2] = "A"
# Set the forth character to 'B':
display[3] = "B"
time.sleep(2)

# Or, can even set the segments to make up characters
# 14-segment raw digits
display.set_digit_raw(0, 0x2D3F)
display.set_digit_raw(1, 0b0010110100111111)
display.set_digit_raw(2, (0b00101101, 0b00111111))
display.set_digit_raw(3, [0x2D, 0x3F])
time.sleep(2)

# Cylon shift left/right testing
display.print('*')
dir = True
pos = 3
for i in range(10):
    display.scroll(1 if dir else -1)
    display.show()
    if dir:
        pos -= 1
        if pos == 0:
            dir = not dir
    else:
        pos += 1
        if pos == 3:
            dir = not dir

    time.sleep(1)

time.sleep(2)
display.print("Fini")
