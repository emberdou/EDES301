"""
--------------------------------------------------------------------------
RGB LCD Test
--------------------------------------------------------------------------
License:   

Copyright 2023 JJ Tellez

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


This code was downloaded from the adafruit library for the LCD and edited.
https://learn.adafruit.com/character-lcds/python-circuitpython
Their licensing information is :
  - SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
  - SPDX-License-Identifier: MIT
--------------------------------------------------------------------------
Use the following hardware components:  
  - RGB backlight positive LCD 16x2  
Requirements:
  - Display messages on screen
Uses:
  - adafruit_character_lcd.character_lcd developed for LCD
  - time
  - board
  - digitalio
  - pwmio
"""

"""Simple test for monochromatic character LCD on PocketBeagle"""
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Pin Config:
lcd_rs = digitalio.DigitalInOut(board.P2_4)
lcd_en = digitalio.DigitalInOut(board.P2_6)
lcd_d7 = digitalio.DigitalInOut(board.P2_5)
lcd_d6 = digitalio.DigitalInOut(board.P2_1)
lcd_d5 = digitalio.DigitalInOut(board.P2_10)
lcd_d4 = digitalio.DigitalInOut(board.P2_8)

lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

def _setup(self):
    """Setup the hardware components."""
    pass

# End def

# Print a two line message
#lcd.color = [0, 100, 0]
lcd.message = "Hello\nCircuitPython"
# Wait 5s
time.sleep(5)
lcd.clear()

# Print two line message right to left
lcd.text_direction = lcd.RIGHT_TO_LEFT
#lcd.color = [100, 0, 0]
lcd.message = "Hello\nCircuitPython"
# Wait 5s
time.sleep(5)
# Return text direction to left to right
lcd.text_direction = lcd.LEFT_TO_RIGHT
# Display cursor
lcd.clear()
lcd.cursor = True
#lcd.color = [0, 0, 100]
lcd.message = "Cursor! "
# Wait 5s
time.sleep(5)
# Display blinking cursor
lcd.clear()
lcd.blink = True
#lcd.color = [0, 100, 0]
lcd.message = "Blinky Cursor!"
# Wait 5s
time.sleep(5)
lcd.blink = False
lcd.clear()
# Create message to scroll
#lcd.color = [100, 0, 0]
scroll_msg = "<-- Scroll"
lcd.message = scroll_msg
# Scroll message to the left
for i in range(len(scroll_msg)):
    time.sleep(0.5)
    lcd.move_left()
lcd.clear()
#lcd.color = [0, 0, 100]
lcd.message = "Going to sleep\nCya later!"
time.sleep(2)