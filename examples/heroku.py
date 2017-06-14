#!/usr/bin/python

import sys
import json
import urllib2
import time
import Adafruit_DHT

FREQUENCY_SECONDS = 60

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 4 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
    api_token = sys.argv[3]
else:
    print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin# api_token')
    print('example: sudo ./Adafruit_DHT.py 2302 4 your-api-token - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)

print('Logging sensor measurements to something every {0} seconds.'.format(FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')

while True:
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Un-comment the line below to convert the temperature to Fahrenheit.
    # temperature = temperature * 9/5.0 + 32

    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        data = {
            'temperature': temperature,
            'humidity': humidity
        }

        req = urllib2.Request('https://better-climate.herokuapp.com')
        req.add_header('Content-Type', 'application/json')
        req.add_header('X-API-TOKEN', api_token)
        urllib2.urlopen(req, json.dumps(data))

        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        time.sleep(2)
        continue

    # Wait 30 seconds before continuing
    time.sleep(FREQUENCY_SECONDS)
