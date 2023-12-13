# Naini's SIOT Coursework

My SKINsense project explored the correlation between various air pollution and weather parameters and skin dryness, as well as present a sensor-IoT infrastructure prototype, which aims to empower users to be aware of the environmental factors contributing to their skin dryness and assist them in taking preventative measures to avoid skin dryness when living in big cities.

## Prototype Setup

The prototype was setup with the following equipment (links to sourced equipment included in embedded links):
* [Raspberry Pi Zero 2 W](https://thepihut.com/products/raspberry-pi-zero-2)
* [Micro SD Card](https://thepihut.com/products/noobs-preinstalled-sd-card)
* [Colour-Coded GPIO Headers](https://thepihut.com/products/colour-coded-gpio-headers)
* [Grove Base HAT for Raspberry Pi Zero](https://thepihut.com/products/grove-base-hat-for-raspberry-pi-zero)
* [GSR Grove Sensor](https://thepihut.com/products/grove-gsr-sensor)
* [HTU21D-F Humidity and Temperature Sensor](https://thepihut.com/products/adafruit-htu21d-f-temperature-humidity-sensor-breakout-board-ada3515)
* Portable power bank
* Micro-USB cable

The following are the steps I took to get the prototype up and running, where `Raspberry Pi Sensor Setup.png` shows the final setup:
1. Solder the GPIO headers onto the Raspberry Pi.
2. Assemble the Grove Base HAT onto the Raspberry Pi, securing with the M3 screws provided. This provides an ADC for the GSR sensor.
3. Assemble the sensor by plugging in the 2-pin grove cable end of the finger part into the mini circuit board 2-pin female connection. Use the other 4-wire grove cable provided - plug one end into the circuit board 4-pin female connection, and the other end into the A0 channel on the grove base HAT.
4. Connect the HTU21D-F to the GPIO pins using male-female jumper:
    * V<sub>in</sub> on the sensor connects to 3.3V pin on the Pi
    * GND on the sensor connects to any GND pin on the Pi
    * SDA on the sensor connects to Pin 3/GPIO 2 (SDA) on the Pi
    * SCL on the sensor connects to Pin 5/GPIO 3 (SCL) on the Pi
5. Flash the Raspberry Pi OS onto the micro SD card, including desktop environment - I did this using the Raspberry Pi Imager for Mac. In the configuration, enter your mobile Internet hotspot connection details.
6. Plug the micro SD card into the Raspberry Pi.
7. Connect the power bank to the Raspberry Pi to power it via the micro-USB cable.
8. Test SSH connection by going to a terminal in any device on the hotspot network, then test connection by entering the following in the terminal, adding the password created during configuration in Step 5:
```
nmandal@Nainis-MBP ~ % ssh naini@nainipi.local
```

The following prerequisites are needed to run the Python Scripts:
* 
