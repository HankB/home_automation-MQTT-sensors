# home_automation-MQTT-sensors

Various scripts and programs to read sensors and publish to the MQTT server 
on oak. Most of these are intended to execute on a Raspberry Pi and read
sensors connected to GPIO pins.

## ds18b20-temp.py

Script to read temperatures from a DS18B20 temperature sensor connected to a Raspberry Pi Zero W and publish to an MQTT server. 

### Status

Reads and publishes on 5 minute schedule and puts out a lot of debug output. At present the script is hard coded for the subject `home_automation/niwot/basement/freezer_temp`.

### TODO

* Make update interval and topic command line arguments.

## frmn.py

Script to read power usage from a TP-Link HS110 smart outlet. (Can run 
on any host since it uses network to collect information.)

### Status

* Reads one sample and reports reply to STDOUT.
* Parse desired info from reply.
* Publish to MQTT server

### TODO

* Make topic command line arguments.
* recover from dropped MQTT server connection.