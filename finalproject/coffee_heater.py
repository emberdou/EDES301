#!/usr/bin/env python3
"""
Coffee Heater Project with Two Heating Pads, LCD, Button, Potentiometer, and DS18B20
Fixed Relay Logic: Starts OFF (HIGH), turns ON (LOW) when heating.
"""

import os
import sys
import time
import glob
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC

# -------------------------
# Load 1-Wire Modules
# -------------------------
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# -------------------------
# DS18B20 Temperature Sensor
# -------------------------
base_dir = '/sys/bus/w1/devices/'
folders = glob.glob(base_dir + '28*')
device_file = None
if folders:
    device_file = os.path.join(folders[0], 'w1_slave')
else:
    print("Warning: No DS18B20 sensor detected; readings will be 0.0")

def read_temp_raw():
    if not device_file:
        return None
    with open(device_file, 'r') as f:
        return f.readlines()

def read_temp():
    if not device_file:
        return None
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    pos = lines[1].find('t=')
    if pos != -1:
        return float(lines[1][pos+2:]) / 1000.0
    return None

# -------------------------
# LCD (4-bit Parallel)
# -------------------------
LCD_RS = "P1_2"
LCD_E = "P1_4"
LCD_D4 = "P2_18"
LCD_D5 = "P2_20"
LCD_D6 = "P2_22"
LCD_D7 = "P2_24"
lcd_pins = [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]

LCD_CMD_CLEAR = 0x01
LCD_CMD_FUNCTION = 0x28
LCD_CMD_DISPLAY_ON = 0x0C
LCD_CMD_ENTRY_MODE = 0x06

def lcd_setup():
    for p in lcd_pins:
        GPIO.setup(p, GPIO.OUT)
    lcd_init()

def lcd_toggle():
    time.sleep(0.001)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(0.001)

def lcd_nibble(n):
    GPIO.output(LCD_D4, GPIO.HIGH if (n & 1) else GPIO.LOW)
    GPIO.output(LCD_D5, GPIO.HIGH if (n & 2) else GPIO.LOW)
    GPIO.output(LCD_D6, GPIO.HIGH if (n & 4) else GPIO.LOW)
    GPIO.output(LCD_D7, GPIO.HIGH if (n & 8) else GPIO.LOW)
    lcd_toggle()

def lcd_byte(b, mode):
    GPIO.output(LCD_RS, GPIO.HIGH if mode else GPIO.LOW)
    lcd_nibble((b >> 4) & 0x0F)
    lcd_nibble(b & 0x0F)
    time.sleep(0.002)

def lcd_init():
    time.sleep(0.02)
    GPIO.output(LCD_RS, GPIO.LOW)
    for _ in range(3):
        lcd_nibble(0x03)
        time.sleep(0.005)
    lcd_nibble(0x02)
    time.sleep(0.001)
    lcd_byte(LCD_CMD_FUNCTION, False)
    lcd_byte(LCD_CMD_DISPLAY_ON, False)
    lcd_byte(LCD_CMD_CLEAR, False)
    lcd_byte(LCD_CMD_ENTRY_MODE, False)
    time.sleep(0.002)

def lcd_message(msg, line=1):
    addr = 0x80 if line == 1 else 0xC0
    lcd_byte(addr, False)
    for c in msg:
        lcd_byte(ord(c), True)

def lcd_clear():
    lcd_byte(LCD_CMD_CLEAR, False)
    time.sleep(0.002)

# -------------------------
# Other Hardware Pins
# -------------------------
BUTTON_PIN = "P1_33"
HEATER1_PIN = "P2_32"
HEATER2_PIN = "P2_34"

heater_enabled = False
_last_button_state = True

def check_button():
    global heater_enabled, _last_button_state
    state = GPIO.input(BUTTON_PIN)
    if state == GPIO.LOW and _last_button_state == GPIO.HIGH:
        heater_enabled = not heater_enabled
        print(f"Heater toggled: {'ON' if heater_enabled else 'OFF'}")  # Debug
        time.sleep(0.2)  # debounce
    _last_button_state = state

def update_heater(cur, want):
    if not heater_enabled:
        GPIO.output(HEATER1_PIN, GPIO.HIGH)  # OFF
        GPIO.output(HEATER2_PIN, GPIO.HIGH)  # OFF
        return "OFF"
    if cur < want:
        GPIO.output(HEATER1_PIN, GPIO.LOW)   # ON
        GPIO.output(HEATER2_PIN, GPIO.LOW)   # ON
        return "HEATING"
    GPIO.output(HEATER1_PIN, GPIO.HIGH)      # OFF
    GPIO.output(HEATER2_PIN, GPIO.HIGH)      # OFF
    return "DONE"

# -------------------------
# Setup & Cleanup
# -------------------------
def setup():
    print(">> STARTING SETUP")
    ADC.setup()
    GPIO.setup(BUTTON_PIN, GPIO.IN)
    for p in (HEATER1_PIN, HEATER2_PIN):
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.HIGH)  # Initialize relays to OFF (HIGH)
    lcd_setup()
    print(">> SETUP COMPLETE")

def cleanup():
    lcd_clear()
    for p in (HEATER1_PIN, HEATER2_PIN):
        GPIO.output(p, GPIO.HIGH)  # Ensure relays are OFF on exit
    GPIO.cleanup()

# -------------------------
# Main Loop
# -------------------------
def main_loop():
    print(">> ENTERING MAIN LOOP")
    while True:
        check_button()
        desired = int(round(ADC.read("P1_19") * 100))
        current = read_temp() or 0.0
        status = update_heater(current, desired)
        
        # Debug prints (check GPIO states)
        h1_state = "ON (LOW)" if GPIO.input(HEATER1_PIN) == GPIO.LOW else "OFF (HIGH)"
        h2_state = "ON (LOW)" if GPIO.input(HEATER2_PIN) == GPIO.LOW else "OFF (HIGH)"
        print(f"DBG: enabled={heater_enabled}, status={status}, set={desired}, now={current:.1f}")
        print(f"DBG: HEATER1={h1_state}, HEATER2={h2_state}")
        
        lcd_message(f"{status} Set:{desired}C", 1)
        lcd_message(f"Now:{current:.1f}C", 2)
        time.sleep(1)

if __name__ == '__main__':
    try:
        setup()
        main_loop()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
        print("Program Complete.")