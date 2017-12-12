#!/usr/bin/python3
'''
Script to fetch current weather from Accuweather, parse it and submit to
the MQTT broker on oak.
Command line arguments
-l --location <location code>
-b --broker <broker host name>
-k --apikey API kep provided by accuweather
-t --test simulate with test response

All arguments required
'''
import argparse
import urllib.request
import json
import sys

import socket
import paho.mqtt.client as mqtt
import time
import pytz
from datetime import datetime

tz = pytz.timezone("US/Central")

verbose = 1

'''
Convert incoming K° to F°
'''
def Kelvin_to_Fahrenheit(k):
    return (k-273)*9/5+32

'''
Application logic
First parse command line arguments
'''

parser = argparse.ArgumentParser()
parser.add_argument('--location', '-l', metavar="<location code>",
                    nargs=1, required=True, help='specify location code')
parser.add_argument('--broker', '-b', metavar="<MQTT broker>",
                    nargs=1, required=True, help='broker host name')
parser.add_argument('--apikey', '-k', metavar="<API key>",
                    nargs=1, required=True, help='broker host name')
parser.add_argument('--test', '-t', # metavar="<test option>",
                    action='store_true', help='use canned response')
parser.add_argument("-v", "--verbosity", 
                    help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
verbose = args.verbosity
if verbose:
    print("location code", args.location[0])
    print("MQTT broker", args.broker[0])
    print("API key", args.apikey[0])
    print("test option", args.test)

"""
Functions related to publishing MQTT messages
"""
topic = "home_automation/"+socket.gethostname()+"/accuweather/weather"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if verbose: print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if verbose: print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    if verbose: print("on_publish(", client, userdata, mid, ")")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect(args.broker[0], 1883, 60)	# connect to my MQTT server

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface. (changed to non-blocking call)
client.loop_start()
### end of included code


def publish_weather(timestamp, temp, humidity, speed, direction): 
    payload = "{0:12.0F}, {1:3.1F}, {2:3.0F}, {3:3.1F}, {4:3.0F}" \
            .format(timestamp,float(temp), float(humidity), float(speed), float(direction))
    if verbose: print("publishing", topic, payload)
    client.publish(topic,payload, qos=0, retain=True)    

''' 
Delay to the next minute interval some integral number of intervals
from time zero.
'''
def delay_to_interval(minutes=15):
    delay_sec = minutes*60 - int(time.time())%(minutes*60)
    time.sleep(delay_sec)

update_interval = 5		# minutes
if not args.test:
    delay_to_interval(update_interval)

# some day loop here. For now just pass through once
while True:    
    timestamp = int(time.time())

    # temporary test code - use canned data to avoid repeated calls to the server
    if args.test == True:
        print("use test data")
        r='[ { "LocalObservationDateTime": "2017-12-11T21:10:00-06:00", "EpochTime": 1513048200, "WeatherText": "Cloudy", "WeatherIcon": 7, "IsDayTime": false, "Temperature": { "Metric": { "Value": 0, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 32, "Unit": "F", "UnitType": 18 } }, "RealFeelTemperature": { "Metric": { "Value": -8.9, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 16, "Unit": "F", "UnitType": 18 } }, "RealFeelTemperatureShade": { "Metric": { "Value": -8.9, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 16, "Unit": "F", "UnitType": 18 } }, "RelativeHumidity": 88, "DewPoint": { "Metric": { "Value": -1.7, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 29, "Unit": "F", "UnitType": 18 } }, "Wind": { "Direction": { "Degrees": 338, "Localized": "NNW", "English": "NNW" }, "Speed": { "Metric": { "Value": 29.6, "Unit": "km/h", "UnitType": 7 }, "Imperial": { "Value": 18.4, "Unit": "mi/h", "UnitType": 9 } } }, "WindGust": { "Speed": { "Metric": { "Value": 29.6, "Unit": "km/h", "UnitType": 7 }, "Imperial": { "Value": 18.4, "Unit": "mi/h", "UnitType": 9 } } }, "UVIndex": 0, "UVIndexText": "Low", "Visibility": { "Metric": { "Value": 8, "Unit": "km", "UnitType": 6 }, "Imperial": { "Value": 5, "Unit": "mi", "UnitType": 2 } }, "ObstructionsToVisibility": "F", "CloudCover": 100, "Ceiling": { "Metric": { "Value": 335, "Unit": "m", "UnitType": 5 }, "Imperial": { "Value": 1100, "Unit": "ft", "UnitType": 0 } }, "Pressure": { "Metric": { "Value": 1011.2, "Unit": "mb", "UnitType": 14 }, "Imperial": { "Value": 29.86, "Unit": "inHg", "UnitType": 12 } }, "PressureTendency": { "LocalizedText": "Rising", "Code": "R" }, "Past24HourTemperatureDeparture": { "Metric": { "Value": 4.4, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 8, "Unit": "F", "UnitType": 18 } }, "ApparentTemperature": { "Metric": { "Value": 0, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 32, "Unit": "F", "UnitType": 18 } }, "WindChillTemperature": { "Metric": { "Value": -6.1, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 21, "Unit": "F", "UnitType": 18 } }, "WetBulbTemperature": { "Metric": { "Value": -0.6, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 31, "Unit": "F", "UnitType": 18 } }, "Precip1hr": { "Metric": { "Value": 0, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0, "Unit": "in", "UnitType": 1 } }, "PrecipitationSummary": { "Precipitation": { "Metric": { "Value": 0, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.01, "Unit": "in", "UnitType": 1 } }, "PastHour": { "Metric": { "Value": 0, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0, "Unit": "in", "UnitType": 1 } }, "Past3Hours": { "Metric": { "Value": 0, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.01, "Unit": "in", "UnitType": 1 } }, "Past6Hours": { "Metric": { "Value": 2, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.08, "Unit": "in", "UnitType": 1 } }, "Past9Hours": { "Metric": { "Value": 2, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.08, "Unit": "in", "UnitType": 1 } }, "Past12Hours": { "Metric": { "Value": 2, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.08, "Unit": "in", "UnitType": 1 } }, "Past18Hours": { "Metric": { "Value": 3, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.13, "Unit": "in", "UnitType": 1 } }, "Past24Hours": { "Metric": { "Value": 3, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.13, "Unit": "in", "UnitType": 1 } } }, "TemperatureSummary": { "Past6HourRange": { "Minimum": { "Metric": { "Value": 0, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 32, "Unit": "F", "UnitType": 18 } }, "Maximum": { "Metric": { "Value": 3.2, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 38, "Unit": "F", "UnitType": 18 } } }, "Past12HourRange": { "Minimum": { "Metric": { "Value": -1.7, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 29, "Unit": "F", "UnitType": 18 } }, "Maximum": { "Metric": { "Value": 4.4, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 40, "Unit": "F", "UnitType": 18 } } }, "Past24HourRange": { "Minimum": { "Metric": { "Value": -8.3, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 17, "Unit": "F", "UnitType": 18 } }, "Maximum": { "Metric": { "Value": 4.4, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 40, "Unit": "F", "UnitType": 18 } } } }, "MobileLink": "http://m.accuweather.com/en/us/winfield-il/60190/current-weather/2256467?lang=en-us", "Link": "http://www.accuweather.com/en/us/winfield-il/60190/current-weather/2256467?lang=en-us" } ]'

    else:
        print("Use real server response")
        url='http://dataservice.accuweather.com/currentconditions/v1/'+args.location[0]+'?apikey='+args.apikey[0]+'&details=true'
        print("URL:", url)
        sys.exit(0)
        req = urllib.request.Request(url)
        r_bytes = urllib.request.urlopen(req).read()
        r = r_bytes.decode('UTF-8')


    ##parsing response
    cont = json.loads(r[1:-1])
    print("cont:", cont)

    counter = 0
    print("\nr:", r)
    #print("cont[name]:", cont['name'])

    print("\ncont[Temperature][Imperial]['Value']:", cont['Temperature']['Imperial']['Value'])
    '''
    print("cont[main][humidity]:", cont['main']['humidity'])
    print("cont[wind][speed]:", cont['wind']['speed'])
    print("cont[wind][deg]:", cont['wind']['deg'])
    print("update time", cont['dt'])

    print(datetime.fromtimestamp(int(cont['dt']), tz).isoformat())
    print(datetime.fromtimestamp(timestamp, tz).isoformat())

    publish_weather(timestamp, temp_F, cont['main']['humidity'], cont['wind']['speed'], cont['wind']['deg'])

    delay_to_interval(update_interval)
    '''
    sys.exit(0)
