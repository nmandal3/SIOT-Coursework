# Naini's SIOT Coursework

My SKINsense project explored the correlation between various air pollution and weather parameters and skin dryness, as well as present a sensor-IoT infrastructure prototype, which aims to empower users to be aware of the environmental factors contributing to their skin dryness and assist them in taking preventative measures to avoid skin dryness when living in big cities.

## Prototype Setup

The prototype was setup with the following equipment (links to sourced equipment included in embedded links):
* [Raspberry Pi Zero 2 W](https://thepihut.com/products/raspberry-pi-zero-2)
* [Micro SD Card](https://thepihut.com/products/noobs-preinstalled-sd-card)
* [Colour-Coded GPIO Headers](https://thepihut.com/products/colour-coded-gpio-headers)
* [Grove Base HAT for Raspberry Pi Zero](https://thepihut.com/products/grove-base-hat-for-raspberry-pi-zero)
* [Galvanic Skin Response (GSR) Grove Sensor](https://thepihut.com/products/grove-gsr-sensor)
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
## Preparing to Run Python Scripts

The following prerequisites are needed to run the Python Scripts:
* Configure the Raspberry Pi to enable I2C interface - I used this [tutorial](https://uk.mathworks.com/help/supportpkg/raspberrypiio/ref/enablei2c.html) by MathWorks.
* Install `raspi-blinka.py` on the Pi - I used this [tutorial](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi) by Adafruit.
* Install the Adafruit CircuitPython HTU21D library - I used this [tutorial](https://learn.adafruit.com/adafruit-htu21d-f-temperature-humidity-sensor/python-circuitpython) by Adafruit.
* Install the Grove ADC library - I used this [tutorial](https://wiki.seeedstudio.com/Grove-GSR_Sensor/) by Seeed Studio.
* Install the Paho MQTT library - I used this [tutoiral](https://bytebeam.io/blog/getting-started-with-mqtt-on-raspberry-pi-using-python/) by Bytebeam.

The following keys are required to retreive data for weather and location, and should be put in lines 61 and 122 of the `/Data Collection with AWS/Files on Naini's Raspberry Pi/sensor2AWS.py` file or line 100 of the `/Data Collection on Local Storage/sensorAPI.py` file:
* [OpenWeather API Key](http://openweathermap.org) - with the student plan, you can get their Developer Plan for free for Weather, which can allow calls for both API pollution and API weather data.
* [IPinfo Token](https://ipinfo.io) - their Free plan is more than enough to collect data.

With the aforementioned steps,`/Data Collection on Local Storage/sensorAPI.py` file can be run. In order to run the `/Data Collection with AWS/Files on Naini's Raspberry Pi/sensor2AWS.py` file can only be run once your AWS is setup, where I have omitted personal connection files (certificates, public-private key pair) and line 55 in the `sensor2AWS.py` file for privacy.

To setup AWS, including IoT Core, DynamoDB and Lambda Functions, I used the following tutorials to help me:
* [Send data from a Raspberry Pi to AWS IoT - Cumulus Cycles](https://youtu.be/XcqVgGXcp4M)
* [Store data sent to AWS IoT in DynamoDB using Lambda - Cumulus Cycles](https://youtu.be/0RcVwTKSbSA)
* [How to Automate Sending Text SMS Notification to Phone Number Using Amazon SNS and AWS Lambda](https://youtu.be/O40eB3K4rPQ)

## How the SKINsense Physical Prototype Works
The prototype was put in a belt bag for convenience as I went about my daily tasks. An image of this can be seen in `Wearable.png`.

### Sensors:
* **GSR Sensor**: Measures skin dryness levels, using finger gloves with electrodes to make contact with skin. The electrical resistance between electrodes decreases with increased skin moisture.
* **HTU21D Sensor**: Measures temperature and humidity sensor and voltage output is a digital signal (therefore an ADC isn't required).
* **IPinfo.io**: Used to call geolocation information about the IP address of the Raspberry Pi (to be replaced with a GPS module as I understand this is very inaccurate).
* **OpenWeather API**: Used to call current weather data for temperature and humidity, and current pollution data for NO<sub>2</sub>, SO<sub>2</sub>, PM10 and PM2.5, all using the geolocation from the previous point.

### Data Collection Process:
* I SSH into my Raspberry Pi from my iPhone using a Terminal app, then run the python script in background to make sure the script keeps running even if I lose internet connection with my Pi:
```
naini@nainipi.local:~ nohup python3 sensor2AWS.py &
```
* A datapoint is sampled with all variables received from the above sensors, attached with a timestamp.
* Data is sampled once every 4 minutes:
    * For the data collection stage, this was done for a 6 hour period (as the prototype is very bulky and intrusive to my daily tasks). After this period, all the collected data is stored in a CSV with the last timestamp.
    * For current data processing, this is in a forever loop, and data gets sent to DynamoDB via publishing to the IoT Core topic `nainirpi/data`, as explained in my report.

## Data Analysis
I used the script `/Data Collection on Local Storage/sensorAPI.py` to retrieve data, as I had only setup my AWS after data collection. The files in `/Raw Data Files` are the result of 6 hour period sampling for each of the 5 days I used the prototype.

I used MATLAB R2021b to carry out data analysis, where I wanted to see the correlation between the environmental variables and GSR sensor data, as well as see if I could make a prediction.

### Basic Time-Series Data Analysis
In `/Data Analysis/Basic Time-Series Data Analysis`, the `sensor_data_all_headings.csv` is a CSV file of manually stitched data of the five raw data files, and the following MATLAB codes were run for basic analysis:
* `plots_unormalised.m` plots the raw data taken, with a plot for each variable, which can be seen in the `/Graphs Plotting Raw Data` folder.
* `plots_overlaid_group` plots the normalised data with 3 graphs overlaying groups, which can be seen in the `/Graphs Plotting Overlaid Data` folder:
    * Sensor temperature and humidity data with GSR
    * API temperature and humidity data with GSR
    * API pollution data with GSR

### Correlation Analysis
In `/Data Analysis/Pearson Correlations without Lag`:
* `pearson_correlations.m` calculates the Pearson Correlation Coefficients (PCC) between all environmental variables and GSR, where the day's CSV file to be inspected can be changed in line 5.
* `PCC Values.png` shows a screenshot of the PCC results after entering each of the five day's data files, which are stored in the variable `resultArray`.

In `/Data Analysis/Time-Lagged Cross Correlations`:
* `time_lagged_correlation.m` evaluates the Time-Lagged Cross Correlation between all environmental variables and GSR, where again the day's CSV file can be changed in line 5.
* `Time-lagged PCC Values.png` shows a screenshot of the peak PCC values at their respective time-lag after entering each of the five day's data files, which are stored in the variable `results`.

### Neural Network Predictions
In `/Data Analysis/Neural Network Modelling`:
* `neural_network_forcasting.m` trains and tests a neural network on one day's data as the training and testing dataset, and predicts GSR values for another day's data as the validation dataset. The days' datasets can be changed in lines 5 and 6.

I didn't manage to finish predictions within the timeframe of the coursework. In addition, it was clear my data could have been more reliable, or at the least, I needed weeks or months of data to make any meaningful data analyses for the context I was studying. Nevertheless, the analyses made can be done again further down the SKINsense project pipeline once more data is collected and prototype refined.
