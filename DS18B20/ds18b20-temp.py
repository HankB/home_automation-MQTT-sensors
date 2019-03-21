#!/usr/bin/python3

""" 
Script to read the temperature from a DS18B20
see https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software
for original code
"""
import glob
import time

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


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
	
# topic = "home_automation/niwot/basement/freezer_temp"
timeStamp = int(time.time())

def publish_temperature(timeStamp, temperature):
    payload = "{0:12.0F}, {1:3.1F}".format(timeStamp,temperature)
    print(payload)

(temp_c, temp_f) = read_temp()
publish_temperature(timeStamp, temp_f)


