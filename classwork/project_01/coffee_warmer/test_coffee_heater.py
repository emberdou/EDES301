# test_coffee_heater.py - Lets you simulate hardware changes
from virtual_hardware import adc, temp_sensor
from coffee_heater import control_loop
import threading

def interactive_control():
    """Let user adjust virtual hardware"""
    while True:
        print("\n1. Set Potentiometer (0-100%)")
        print("2. Set Current Temperature")
        print("3. Exit")
        choice = input("Select: ")
        
        if choice == "1":
            value = int(input("Enter pot % (0-100): "))
            adc.set_pot_value(value)
        elif choice == "2":
            temp = float(input("Enter temperature (°C): "))
            temp_sensor.set_temp(temp)
        elif choice == "3":
            break

if __name__ == '__main__':
    # Start coffee heater in background
    heater_thread = threading.Thread(target=control_loop)
    heater_thread.daemon = True
    heater_thread.start()
    
    # Start interactive control
    interactive_control()