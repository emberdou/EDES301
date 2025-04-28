This is the code for the coffee heater. The tempsensor.dtbo is how the one wire configuration is set up. configure_pins is used for the temperature sensor, the rest are in the code already. This is running on python 3.11 

https://www.hackster.io/elb10/pocket-beagle-coffee-heater-bcebcc

This is some of the things you will need to run 

Adafruit libraries
sudo pip3 install --upgrade setuptools --> sudo pip3 install --upgrade Adafruit_BBIO --> sudo pip3 install adafruit-blinka

Temperature sensor
Download the DTS file for the DS18B20 temperature sensor. Run the code below to set up for the temperature sensor: debian@beaglebone:/boot$ cat uEnv.txt --> debian@beaglebone:/var/lib/cloud9$ cd /sys/bus --> debian@beaglebone:/sys/bus$ ls --> debian@beaglebone:/sys/bus$ cd w1 --> debian@beaglebone:/sys/bus/w1$ ls --> debian@beaglebone:/sys/bus/w1$ cd devices --> debian@beaglebone:/sys/bus/w1/devices$ ls --> debian@beaglebone:/sys/bus/w1/devices$ cd 28-20a9d4469694 --> debian@beaglebone:/sys/bus/w1/devices/28-20a9d4469694 ls --> debian@beaglebone:/sys/bus/w1/devices/28-20a9d4469694$ ls --> debian@beaglebone:/sys/bus/w1/devices/28-20a9d4469694$ cat w1_slave


