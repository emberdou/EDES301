#!/bin/bash

# setup_hardware.sh - One-time hardware configuration

# Configure pins
sudo config-pin P1_19 adc    # Potentiometer
sudo config-pin P1_26 i2c    # LCD SCL
sudo config-pin P1_28 i2c    # LCD SDA

# Enable 1-Wire for temperature sensor
echo "wire" | sudo tee /sys/devices/platform/bone_capemgr/slots >/dev/null

echo "Hardware configuration complete"