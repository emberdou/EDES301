"""
--------------------------------------------------------------------------
Coffee Heater Project
--------------------------------------------------------------------------
License:   
2025 Emma Berdou
Credit to Alvaro Castillo 2018 

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
--------------------------------------------------------------------------

"""
import sys
sys.path.append("/var/lib/cloud9/EDES301/i2c/") # Path for the hex display library

import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import smbus
import os
import glob

# --- LCD Configuration (I2C) ---
LCD_ADDRESS = 0x27  # Try 0x3F if this doesn't work
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_BACKLIGHT = 0x08
bus = smbus.SMBus(2)  # PocketBeagle I2C bus 2

# --- GPIO Pins ---
HEATER_PIN = "P2_24"
POT_PIN = "P1_19"     # Potentiometer

# --- Temperature Sensor ---
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# ================= LCD FUNCTIONS =================
def lcd_init():
    """Initialize the LCD"""
    try:
        lcd_byte(0x33, LCD_CMD)  # Initialize
        lcd_byte(0x32, LCD_CMD)  # Set to 4-bit mode
        lcd_byte(0x28, LCD_CMD)  # 2 lines, 5x8 matrix
        lcd_byte(0x0C, LCD_CMD)  # Display on, cursor off
        lcd_byte(0x06, LCD_CMD)  # Cursor move direction
        lcd_byte(0x01, LCD_CMD)  # Clear display
        time.sleep(0.2)
    except:
        print("LCD init failed")

def lcd_byte(bits, mode):
    """Send byte to LCD"""
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT
    
    bus.write_byte(LCD_ADDRESS, bits_high)
    lcd_toggle_enable(bits_high)
    bus.write_byte(LCD_ADDRESS, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    """Toggle enable pin"""
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDRESS, (bits | 0x04))
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDRESS, (bits & ~0x04))
    time.sleep(0.0005)

def lcd_string(message, line):
    """Print string to LCD"""
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)

# ================= SYSTEM FUNCTIONS =================
def setup():
    """Initialize hardware"""
    GPIO.setup(HEATER_PIN, GPIO.OUT)
    GPIO.output(HEATER_PIN, GPIO.LOW)
    ADC.setup()
    lcd_init()
    lcd_string("Coffee Heater", LCD_LINE_1)
    lcd_string("Initializing...", LCD_LINE_2)
    time.sleep(2)

def read_temp():
    """Read DS18B20 temperature"""
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
            if lines[0].strip()[-3:] == 'YES':
                temp_pos = lines[1].find('t=')
                if temp_pos != -1:
                    return float(lines[1][temp_pos+2:]) / 1000.0
        return 0.0
    except:
        return 0.0

def update_display(current_temp, set_temp, heating):
    """Update LCD with system status"""
    # Line 1: Current temperature
    lcd_string(f"Now: {current_temp:.1f}C", LCD_LINE_1)
    
    # Line 2: Set temperature and status
    status = "HEATING" if heating else "READY "
    lcd_string(f"Set: {set_temp:.0f}C {status}", LCD_LINE_2)

def cleanup():
    """Turn everything off"""
    lcd_string("System Off", LCD_LINE_1)
    lcd_string("", LCD_LINE_2)
    GPIO.output(HEATER_PIN, GPIO.LOW)
    bus.close()

# ================= MAIN LOOP =================
def main():
    try:
        setup()
        last_pot_value = 0
        
        while True:
            # Read potentiometer value (0-100°C)
            pot_value = round(ADC.read(POT_PIN) * 100, 1)
            if abs(pot_value - last_pot_value) >= 0.5:
                last_pot_value = pot_value
            
            current_temp = read_temp()
            
            # Control logic with hysteresis
            if current_temp < (last_pot_value - 1):  # 1°C below target
                heating = True
                GPIO.output(HEATER_PIN, GPIO.HIGH)
            else:
                heating = False
                GPIO.output(HEATER_PIN, GPIO.LOW)
            
            # Update display every 0.5s
            update_display(current_temp, last_pot_value, heating)
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == '__main__':
    main()