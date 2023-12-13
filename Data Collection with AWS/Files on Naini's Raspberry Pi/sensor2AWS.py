import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

import requests
from datetime import datetime
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
            return round(self.sensor.temperature, 2)
        except Exception as e:
            print(f"Error reading temperature: {e}")
            return None

    @property
    def humidity(self):
        try:
            return round(self.sensor.relative_humidity, 2)
        except Exception as e:
            print(f"Error reading humidity: {e}")
            return None

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt', keyfile='./private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("ommitted for privacy.amazonaws.com", 8883, 60)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_local_position():
    ipinfo_token = 'ommitted for privacy'
    try:
        # Use IPinfo API to get geolocation based on IP
        response = requests.get(f'http://ipinfo.io?token={ipinfo_token}')
        data = response.json()
        
        # Extract lat and long from the response
        lat, lon = map(float, data['loc'].split(','))
        
        return lat, lon
    except Exception as e:
        # If an error occurs, return default values for Ealing, GB
        print(f"Error getting local position: {e}")
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
        response.raise_for_status()  # Check for errors in the response
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
        response.raise_for_status()  # Check for errors in the response
        weather_data = response.json()

        temperature = round(weather_data['main']['temp'] - 273.15, 2) 
        humidity = weather_data['main']['humidity']
    except (requests.RequestException, KeyError):
        temperature, humidity = None, None

    return temperature, humidity

#duration = 60*60*1  # Duration in seconds (1 hour)
interval = 60*4  # Sampling interval in seconds (4 mins)
#samples = duration // interval
api_key = "ommitted for privacy"

sensor1 = GroveGSRSensor()  # GSR sensor on A0 channel
sensor2 = HumidityTemperatureSensor()  # HTU21D sensor using I2C bus

def publishData(txt):
    print(txt)
    while (True):
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

        payload = {
            "timestamp" : timestamp,
            "gsr": gsr_value,
            "stemp": temperature_sensor,
            "shumidity": humidity_sensor,
            "apitemperature": temperature_api,
            "apihumidity": humidity_api,
            "so2": so2,
            "no2": no2,
            "pm10": pm10,
            "pm25": pm25
        }

        print(f'{timestamp} - GSR value: {gsr_value}')
        print(f'{timestamp} - Sensor Temperature: {temperature_sensor:.1f} C' if temperature_sensor is not None else f'{timestamp} - Sensor Temperature: None')
        print(f'{timestamp} - Sensor Humidity: {humidity_sensor:.1f} %' if humidity_sensor is not None else f'{timestamp} - Sensor Humidity: None')
        print(f'{timestamp} - API Temperature: {temperature_api}' if temperature_api is not None else f'{timestamp} - API Temperature: None')
        print(f'{timestamp} - API Humidity: {humidity_api}' if humidity_api is not None else f'{timestamp} - API Humidity: None')
        print(f'{timestamp} - SO2: {so2}' if so2 is not None else f'{timestamp} - SO2: None')
        print(f'{timestamp} - NO2: {no2}' if no2 is not None else f'{timestamp} - NO2: None')
        print(f'{timestamp} - PM10: {pm10}' if pm10 is not None else f'{timestamp} - PM10: None')
        print(f'{timestamp} - PM2.5: {pm25}' if pm25 is not None else f'{timestamp} - PM2.5: None')

        client.publish("nainirpi/data",
            payload=json.dumps(payload),
            qos=1, retain=False
        )
        
        time.sleep(interval)

_thread.start_new_thread(publishData,("Spin-up new Thread...",))

client.loop_forever()
