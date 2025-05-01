# virtual_hardware.py - Simulates hardware for testing
import random

class VirtualGPIO:
    def __init__(self):
        self.pins = {}
        
    def setup(self, pin, mode):
        self.pins[pin] = {"mode": mode, "value": 0}
        
    def output(self, pin, value):
        if pin in self.pins:
            self.pins[pin]["value"] = value
        else:
            print(f"Virtual pin {pin} not set up!")
            
    def cleanup(self):
        self.pins.clear()

class VirtualADC:
    def __init__(self):
        self.pot_value = 50  # Default 50% rotation
        
    def read(self, pin):
        # Returns 0.0-1.0 simulating potentiometer
        return self.pot_value / 100.0
        
    def set_pot_value(self, value):
        # For testing: set virtual pot position (0-100)
        self.pot_value = max(0, min(100, value))

class VirtualTempSensor:
    def __init__(self):
        self.current_temp = 20.0  # Start at 20°C
        
    def read_temp(self):
        # Simulate small temp fluctuations
        self.current_temp += random.uniform(-0.5, 0.5)
        return round(self.current_temp, 1)
        
    def set_temp(self, temp):
        self.current_temp = temp

# Global simulated hardware
gpio = VirtualGPIO()
adc = VirtualADC()
temp_sensor = VirtualTempSensor()