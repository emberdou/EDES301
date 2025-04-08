#!/usr/bin/env python3
# coffee_heater_virtual.py - Complete self-contained simulator

import time
import random
import threading

# ================= VIRTUAL HARDWARE SIMULATION =================
class VirtualHardware:
    def __init__(self):
        # Simulated hardware state
        self.pot_value = 50       # 50% potentiometer
        self.current_temp = 20.0  # Starting at 20°C
        self.heater_on = False
        self.running = True

    # ---- Simulated Hardware Methods ----
    def read_potentiometer(self):
        """Returns 0.0-1.0 simulating pot rotation"""
        return self.pot_value / 100.0

    def read_temperature(self):
        """Returns temperature with small random fluctuations"""
        self.current_temp += random.uniform(-0.2, 0.2)
        return round(self.current_temp, 1)

    def set_heater(self, state):
        """Turns virtual heater on/off"""
        self.heater_on = state
        # Temperature rises faster when heater is on
        if state:
            self.current_temp += 0.5

    # ---- Control Methods ----
    def set_potentiometer(self, value):
        """For testing: set virtual pot position (0-100)"""
        self.pot_value = max(0, min(100, value))

    def set_temperature(self, temp):
        """For testing: manually set temperature"""
        self.current_temp = temp

# ================= COFFEE HEATER LOGIC =================
class VirtualCoffeeHeater:
    def __init__(self):
        self.hw = VirtualHardware()
        self.update_interval = 1.0  # seconds

    def run(self):
        """Main control loop"""
        try:
            while self.hw.running:
                # Get desired temp from virtual pot (0-100°C)
                desired_temp = round(self.hw.read_potentiometer() * 100, 1)
                
                # Get current temp
                current_temp = self.hw.read_temperature()
                
                # Control logic
                if current_temp < desired_temp:
                    self.hw.set_heater(True)
                    status = "HEATING"
                else:
                    self.hw.set_heater(False)
                    status = "READY "
                
                # Display status
                self._print_status(desired_temp, current_temp, status)
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            self.hw.running = False

    def _print_status(self, target, current, status):
        """Clear console and display status"""
        print("\033[H\033[J")  # Clear console
        print("=== VIRTUAL COFFEE HEATER ===")
        print(f"Target Temp: {target}°C")
        print(f"Current Temp: {current}°C")
        print(f"\nStatus: {status}")
        print(f"Heater: {'ON' if self.hw.heater_on else 'OFF'}")
        print("\nControls:")
        print("1. Adjust Potentiometer")
        print("2. Set Temperature")
        print("3. Exit")

# ================= INTERACTIVE TEST INTERFACE =================
def interactive_control(heater):
    """User interface for testing"""
    while heater.hw.running:
        choice = input("\nSelect option (1-3): ")
        
        if choice == "1":
            value = int(input("Set potentiometer % (0-100): "))
            heater.hw.set_potentiometer(value)
        elif choice == "2":
            temp = float(input("Set temperature (°C): "))
            heater.hw.set_temperature(temp)
        elif choice == "3":
            heater.hw.running = False
            break

# ================= MAIN EXECUTION =================
if __name__ == '__main__':
    heater = VirtualCoffeeHeater()
    
    # Start heater in background thread
    heater_thread = threading.Thread(target=heater.run)
    heater_thread.daemon = True
    heater_thread.start()
    
    # Start interactive control
    interactive_control(heater)
    
    print("\nVirtual coffee heater stopped.")