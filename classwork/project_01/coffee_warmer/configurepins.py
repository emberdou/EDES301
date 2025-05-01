#!/usr/bin/env python3
# config_pins.py - Hardware pin configuration for Coffee Heater

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC

def setup_pins():
    """Configure all hardware pins"""
    
    # ADC/Potentiometer
    ADC.setup()
    
    # GPIO Pins
    GPIO.setup("P2_24", GPIO.OUT)  # Heater control
    GPIO.output("P2_24", GPIO.LOW)  # Start with heater off
    
    # I2C (for LCD) - No direct pin setup needed
    # Temperature sensor (1-Wire) - Configured via device tree overlay

def cleanup_pins():
    """Clean up all GPIO resources"""
    GPIO.output("P2_24", GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    # For testing pin configuration
    print("Configuring pins...")
    setup_pins()
    input("Press Enter to clean up pins...")
    cleanup_pins()
    print("Done")