#!/usr/bin/env python3
"""
parallel_lcd_test.py

Minimal HD44780 16×2 parallel test on PocketBeagle using Adafruit_BBIO.GPIO.
"""

import time
import Adafruit_BBIO.GPIO as GPIO

# Pin mapping
LCD_RS = "P1_2"
LCD_E  = "P1_4"
LCD_D4 = "P2_18"
LCD_D5 = "P2_20"
LCD_D6 = "P2_22"
LCD_D7 = "P2_24"

ALL_PINS = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

# HD44780 Commands
CMD_CLEAR      = 0x01
CMD_FUNCTION   = 0x28  # 4‑bit, 2 lines, 5×8 dots
CMD_DISPLAY_ON = 0x0C  # Display ON, cursor OFF, blink OFF
CMD_ENTRY_MODE = 0x06  # Increment cursor

def setup():
    # Configure pins as outputs
    for p in ALL_PINS:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.LOW)
    lcd_init()

def lcd_toggle_enable():
    time.sleep(0.001)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(0.001)

def lcd_send_nibble(n):
    GPIO.output(LCD_D4, GPIO.HIGH if (n & 0x1) else GPIO.LOW)
    GPIO.output(LCD_D5, GPIO.HIGH if (n & 0x2) else GPIO.LOW)
    GPIO.output(LCD_D6, GPIO.HIGH if (n & 0x4) else GPIO.LOW)
    GPIO.output(LCD_D7, GPIO.HIGH if (n & 0x8) else GPIO.LOW)
    lcd_toggle_enable()

def lcd_send_byte(b, is_data):
    GPIO.output(LCD_RS, GPIO.HIGH if is_data else GPIO.LOW)
    lcd_send_nibble((b >> 4) & 0x0F)
    lcd_send_nibble(b & 0x0F)
    time.sleep(0.002)

def lcd_init():
    time.sleep(0.02)  # wait >15ms after power-on
    # Initialize in 4-bit mode
    for _ in range(3):
        lcd_send_nibble(0x03)
        time.sleep(0.005)
    lcd_send_nibble(0x02)
    time.sleep(0.001)
    # Function set, display control, clear, entry mode
    lcd_send_byte(CMD_FUNCTION,   False)
    lcd_send_byte(CMD_DISPLAY_ON, False)
    lcd_send_byte(CMD_CLEAR,      False)
    lcd_send_byte(CMD_ENTRY_MODE, False)

def lcd_message(text, line=1):
    addr = 0x80 if line == 1 else 0xC0
    lcd_send_byte(addr, False)
    for char in text.ljust(16):
        lcd_send_byte(ord(char), True)

def cleanup():
    # Clear display and release pins
    lcd_send_byte(CMD_CLEAR, False)
    time.sleep(0.002)
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        lcd_message("are u dtf!", 1)
        lcd_message("slide.",   2)
        time.sleep(5)
    finally:
        cleanup()
