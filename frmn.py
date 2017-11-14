#!/usr/bin/env python

"""
Monitor TP-Link HS-100 smartplug to determine when freezer door is left ajar

Some of this code (validIP, encrypot, decrypt and contents of sendrecv) are
copied from tplink-smartplug.py
(https://github.com/softScheck/tplink-smartplug)

"""

import socket
import argparse
import paho.mqtt.client as mqtt
import re
import time

version = 0.2

"""
Functions related to communicating with TP-Link socket
"""

# Check if IP is valid
def validIP(ip):
	try:
		socket.inet_pton(socket.AF_INET, ip)
	except socket.error:
		parser.error("Invalid IP Address.")
	return ip 

# see if we can resolve host
def validHost(h):
    try:
        addr = socket.gethostbyname(h)
    except:
        parser.error("could not resolve host "+ h)
    return addr
        

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
	key = 171
	result = "\0\0\0\0"
	for i in string: 
		a = key ^ ord(i)
		key = a
		result += chr(a)
	return result

def decrypt(string):
	key = 171 
	result = ""
	for i in string: 
		a = key ^ ord(i)
		key = ord(i) 
		result += chr(a)
	return result

# Send command and receive reply 
def sendrecv(cmd):
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((addr, port))
        sock_tcp.send(encrypt(cmd))
        data = sock_tcp.recv(2048)
        sock_tcp.close()

        reply = decrypt(data[4:])
        return reply
    except socket.error:
        return None

"""
Functions related to publishing MQTT messages
"""
topic = "home_automation/"+socket.gethostname()+"/basement/freezer_power"

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

def publish_power(timestamp, I, V, W): # I, V, P => amps, volts. watts
    payload = "{0:12.0F}, {1:3.2F}, {2:3.1F}, {3:3.1F}" \
            .format(timestamp,float(I), float(V), float(W))
    print("publishing", payload)
    client.publish(topic,payload, qos=0, retain=True)    

""" 
Delay to the next minute interval some integral number of intervals
from time zero.
"""
def delay_to_interval(minutes=15):
    delay_sec = minutes*60 - int(time.time())%(minutes*60)
    time.sleep(delay_sec)


"""
Application logic
"""

# Parse commandline arguments
parser = argparse.ArgumentParser(description="Freezer monitor v" + str(version))
host = parser.add_mutually_exclusive_group(required=True)
host.add_argument("-t", "--target", metavar="<ip>", help="Target IP Address", type=validIP)
host.add_argument("-n", "--name", metavar="<name>", help="Target host name", type=validHost)
args = parser.parse_args()

ip = args.target
port = 9999
if args.target is None:
    print("Using ", args.name)
    addr = args.name
else:
    print("Using ", args.target)
    addr = args.target
    
update_interval = 5		# minutes
delay_to_interval(update_interval)

while True:    
    timestamp = int(time.time())
    reply = sendrecv('{"emeter":{"get_realtime":{}}}')
    # parse reply which looks like
    # {"emeter":{"get_realtime":{"current":1.743814,"voltage":123.531411,"power":112.291943,"total":15.761000,"
    print(reply)
    fields=re.split('[:,]', reply) # isolate readings from the string
    if len(fields) != 12 or fields[0] != '{"emeter"':
        print("Unexpected reply:\n   ", reply)
        current = voltage = power = 0
    else:
        current = fields[3]
        voltage = fields[5]
        power = fields[7]

    print("c,v,p", current, voltage, power)
    publish_power(timestamp, current, voltage, power)
    delay_to_interval(update_interval)
