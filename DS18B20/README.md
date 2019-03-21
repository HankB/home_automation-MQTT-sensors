# Support DS18B20 sensor

This is used to monitor the basement freezer temperature. Related to this is
a script that monitors power usage for the freezer using a TP-Link HS110. (in
`.../home_automation-MQTT-sensors/energy`)

## Strategy

Use the DS18B20 temperature sensor to read freezer temperature. Write the result to STDOUT in a format suitable tp pipe to `mosquitto_pub` to publish to the MQTT broker on `oak`.

## Components

### ds18b20-temp.py

See https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

Script to read temperatures from a DS18B20 temperature sensor connected to a Raspberry Pi and publish to an MQTT server. This works with any Raspberry Pi which has network connectivity including a Pi Zero with USB WiFi dongle or Pi Zero W.

#### Requirements

Enable 1 wire interface

* Add `dtoverlay=w1-gpio` to the end of `/boot/config.txt`.

#### Status

Work in progress to convert to a script that reads temperature and writes to STDOUT
in order to publish using mosquitto_pub.

#### TODO

* Continue with restructuring
* Write shell script to orchestrate.
