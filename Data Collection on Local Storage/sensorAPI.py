import time
import requests
from datetime import datetime
import csv
from adc import ADC
import board
from adafruit_htu21d import HTU21D

class GroveGSRSensor:
    def __init__(self, channel=0):
        self.channel = channel
        self.adc = ADC()

    @property
    def GSR(self):
        try:
            value = self.adc.read(self.channel)
            return value
        except Exception as e:
            print(f"Error reading GSR: {e}")
            return None

class HumidityTemperatureSensor:
    def __init__(self):
        self.i2c = board.I2C()
        self.sensor = HTU21D(self.i2c)

    @property
    def temperature(self):
        try:
            return self.sensor.temperature
        except Exception as e:
            print(f"Error reading temperature: {e}")
            return None

    @property
    def humidity(self):
        try:
            return self.sensor.relative_humidity
        except Exception as e:
            print(f"Error reading humidity: {e}")
            return None


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_local_position():
    # Code to obtain local position data from the Raspberry Pi
    # If not possible, return default values for Ealing, GB
    return 51.509865, -0.118092  # Ealing, London, GB

def get_air_pollution(api_key, lat, lon):
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        pollution_data = response.json()

        components = pollution_data['list'][0]['components']
        so2 = components.get('so2')
        no2 = components.get('no2')
        pm10 = components.get('pm10')
        pm25 = components.get('pm2_5')
    except (requests.RequestException, KeyError, IndexError):
        so2, no2, pm10, pm25 = None, None, None, None

    return so2, no2, pm10, pm25

def get_weather(api_key, lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
    except (requests.RequestException, KeyError):
        temperature, humidity = None, None

    return temperature, humidity

def main():
    duration = 60*60*6  # Duration in seconds (6 hours)
    interval = 60*4  # Sampling interval in seconds (4 mins)
    samples = duration // interval
    api_key = "ommitted for privacy"

    sensor1 = GroveGSRSensor()  # GSR sensor on A0 channel
    sensor2 = HumidityTemperatureSensor()  # HTU21D sensor using I2C bus

    data = []

    print('Detecting...')
    for _ in range(samples):
        timestamp = get_timestamp()
        gsr_value = sensor1.GSR
        temperature_sensor = sensor2.temperature
        humidity_sensor = sensor2.humidity
		
		# Get local position data or use default values
        lat, lon = get_local_position()

		# Get air pollution data
        so2, no2, pm10, pm25 = get_air_pollution(api_key, lat, lon)

		# Get weather data
        temperature_api, humidity_api = get_weather(api_key, lat, lon)
		
        #data.append([timestamp, gsr_value, temperature_sensor, humidity_sensor, temperature_api, humidity_api, so2, no2, pm10, pm25])

        data.append([
            timestamp,
            gsr_value if gsr_value is not None else "None",
            temperature_sensor if temperature_sensor is not None else "None",
            humidity_sensor if humidity_sensor is not None else "None",
            temperature_api if temperature_api is not None else "None",
            humidity_api if humidity_api is not None else "None",
            so2 if so2 is not None else "None",
            no2 if no2 is not None else "None",
            pm10 if pm10 is not None else "None",
            pm25 if pm25 is not None else "None",
        ])
        print('{0} - GSR value: {1}'.format(timestamp, gsr_value))
        print('{0} - Sensor Temperature: {1}'.format(timestamp, f'{temperature_sensor:.1f} C' if temperature_sensor is not None else 'None'))
        print('{0} - Sensor Humidity: {1}'.format(timestamp, f'{humidity_sensor:.1f} %' if humidity_sensor is not None else 'None'))
        print('{0} - API Temperature: {1}'.format(timestamp, temperature_api))
        print('{0} - API Humidity: {1}'.format(timestamp, humidity_api))
        print('{0} - SO2: {1}'.format(timestamp, so2))
        print('{0} - NO2: {1}'.format(timestamp, no2))
        print('{0} - PM10: {1}'.format(timestamp, pm10))
        print('{0} - PM2.5: {1}'.format(timestamp, pm25))
        
        time.sleep(interval)

    # Write data to CSV file
    csv_filename = f'sensor_data_{get_timestamp()}.csv'
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'GSR', 'Sensor Temperature (C)', 'Sensor Humidity (%)', 'API Temperature (K)', 'API Humidity (%)', 'SO2', 'NO2', 'PM10', 'PM2.5'])
        csv_writer.writerows(data)

    print(f'Data written to {csv_filename}')

if __name__ == '__main__':
    main()
