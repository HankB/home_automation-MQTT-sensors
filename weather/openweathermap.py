#!/usr/bin/python3
'''
Script to fetch current weather from OpenWeatherMap, parse it and submit to
the MQTT broker on oak.
Command line arguments
-z --zipcode <zip code>
-b --broker <broker host name>
-k --apikey API kep provided by accuweather
-t --test simulate with test response

All arguments except '-t' required
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
parser.add_argument('--zip', '-z', metavar="<zipcode>",
                    nargs=1, required=True, help='specify zip code')
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
    print("zip code", args.zip[0])
    print("MQTT broker", args.broker[0])
    print("API key", args.apikey[0])
    print("test option", args.test)

"""
Functions related to publishing MQTT messages
"""
topic = "home_automation/"+socket.gethostname()+"/openweathermap/weather"

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
delay_to_interval(update_interval)

# some day loop here. For now just pass through once
while True:    
    timestamp = int(time.time())

    # temporary test code - use canned data to avoid repeated calls to the server
    if args.test == True:
        print("use test data")
        r='{"coord":{"lon":-88.15,"lat":41.87},"weather":[{"id":804,"main":   "Clouds","description":"overcast clouds","icon":"04n"}],"base":"stations",    "main":{"temp":272.05,"pressure":1018,"humidity":68,"temp_min":271.15,"temp_max":273.15},"visibility":16093,"wind":{"speed":2.6,"deg":340},"clouds":{"all":90},"dt":1512953100,"sys":{"type":1,"id":1007,"message":0.1736,"country":"US","sunrise":1512997823,"sunset":1513030899},"id":0,"name":"Winfield","cod":200}'

    else:
        print("Use real server response")
        url='http://api.openweathermap.org/data/2.5/weather?zip='+args.zip[0]+'&apikey='+args.apikey[0]
        print("URL:", url)
        req = urllib.request.Request(url)
        print("req:", req)
        r_bytes = urllib.request.urlopen(req).read()
        r = r_bytes.decode('UTF-8')


    ##parsing response
    cont = json.loads(r)
    print("cont:", cont)

    counter = 0
    print("\nr:", r)
    print("cont[name]:", cont['name'])

    temp_F = Kelvin_to_Fahrenheit(cont['main']['temp'])
    print("\ncont[main][temp]:", temp_F)
    print("cont[main][humidity]:", cont['main']['humidity'])
    print("cont[wind][speed]:", cont['wind']['speed'])
    print("cont[wind][deg]:", cont['wind']['deg'])
    print("update time", cont['dt'])

    print(datetime.fromtimestamp(int(cont['dt']), tz).isoformat())
    print(datetime.fromtimestamp(timestamp, tz).isoformat())

    publish_weather(timestamp, temp_F, cont['main']['humidity'], cont['wind']['speed'], cont['wind']['deg'])

    delay_to_interval(update_interval)
