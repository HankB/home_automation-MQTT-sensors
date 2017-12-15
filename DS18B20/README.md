# Support DS18B20 sensor
This is used to monitor the basement freezer temperature. Related to this is
a script that monitors power usage for the freezer using a TP-Link HS110.

## Modules
### ds18b20-temp.py
See https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

Script to read temperatures from a DS18B20 temperature sensor connected to a Raspberry Pi and publish to an MQTT server. This works with any Raspberry Pi which has network connectivity including a Pi Zero with USB WiFi dongle or Pi Zero W.

#### Requirements
Install paho-mqtt following instructions at https://www.eclipse.org/paho/clients/python/.

Enable 1 wire interface
* Add `dtoverlay=w1-gpio` to the end of `/boot/config.txt`.
#### Status

Reads and publishes on 5 minute schedule and puts out a lot of debug output. At present the script is hard coded for the subject `home_automation/niwot/basement/freezer_temp`.

#### TODO

* Make update interval and topic command line arguments.

### frmn.py

Script to read power usage from a TP-Link HS110 smart outlet. (Can run
on any host since it uses network to collect information.)

#### Requirements

* paho-mqtt module as above.
#### Status

* Reads one sample and reports reply to STDOUT.
* Parse desired info from reply.
* Publish to MQTT server
#### TODO

* Update TODO list ;)
* Done - Make topic command line arguments.
* <s>Recover from dropped MQTT server connection.</s>
* Open/Close connection for each sample to send.
* Investigate switch to libmosquitto