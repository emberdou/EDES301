# coffee_heater.py - Now works without physical hardware
from virtual_hardware import gpio, adc, temp_sensor
import time

# Configuration
HEATER_PIN = "P2_24"
POT_PIN = "P1_19"
UPDATE_INTERVAL = 1.0  # seconds

def setup():
    """Initialize virtual hardware"""
    gpio.setup(HEATER_PIN, "output")
    print("Virtual hardware initialized")
    print(f"Potentiometer: {adc.pot_value}%")
    print(f"Current temp: {temp_sensor.current_temp}°C")

def read_temp():
    """Get simulated temperature"""
    return temp_sensor.read_temp()

def control_loop():
    """Main control logic"""
    try:
        while True:
            # Get desired temp from virtual pot (0-100°C)
            desired_temp = round(adc.read(POT_PIN) * 100, 1)
            
            # Get current temp
            current_temp = read_temp()
            
            # Control logic
            if current_temp < desired_temp:
                gpio.output(HEATER_PIN, 1)
                status = "HEATING"
            else:
                gpio.output(HEATER_PIN, 0)
                status = "READY "
            
            # Display status
            print(f"\nSet Temp: {desired_temp}°C")
            print(f"Cur Temp: {current_temp}°C")
            print(f"Status: {status}")
            print(f"Heater: {'ON' if gpio.pins[HEATER_PIN]['value'] else 'OFF'}")
            
            time.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        pass

def cleanup():
    """Clean up virtual hardware"""
    gpio.cleanup()
    print("\nVirtual hardware cleaned up")

if __name__ == '__main__':
    setup()
    try:
        control_loop()
    finally:
        cleanup()