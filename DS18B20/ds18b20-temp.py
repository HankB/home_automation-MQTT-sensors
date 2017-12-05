#!/usr/bin/python3

""" 
Script to read the temperature from a DS18B20
see https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software
for original code
"""
import glob
import time

### copied from https://www.eclipse.org/paho/clients/python/
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    print("on_publish(", client, userdata, mid, ")")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect("oak", 1883, 60)	# connect to my MQTT server

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface. (changed to non-blocking call)
client.loop_start()
### end of included code


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
update_interval = 5		# minutes


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
	
""" 
Delay to the next minute interval some integral number of intervals
from time zero.
"""
def delay_to_interval(minutes=15):
    delay_sec = minutes*60 - int(time.time())%(minutes*60)
    time.sleep(delay_sec)

topic = "home_automation/niwot/basement/freezer_temp"

def publish_temperature(timestamp, temperature):
    payload = "{0:12.0F}, {1:3.1F}".format(timestamp,temperature)
    print("publishing", payload)
    client.publish(topic,payload, qos=0, retain=True)    

delay_to_interval(update_interval)

print("starting main loop")

while True:
    timeStamp = int(time.time())
    temp = read_temp()[1]
    print(timeStamp, temp)
    publish_temperature(timeStamp, temp)
    delay_to_interval(update_interval)
