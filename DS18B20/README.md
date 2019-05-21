# Support DS18B20 sensor

This is used to monitor the basement freezer temperature. Related to this is
a script that monitors power usage for the freezer using a TP-Link HS110. (in
`.../home_automation-MQTT-sensors/energy`)

## Strategy

Use the DS18B20 temperature sensor to read freezer temperature. Write the result to STDOUT in a format suitable tp pipe to `mosquitto_pub` to publish to the MQTT broker on `oak`.

## Usage

* Copy `ds18b20-temp.py` and `publish-freezer-temp.sh` to `/home/pi/bin`.
* Add a cron job to execute on the desired interval.

```cron
*/5 * * * * /home/pi/bin/publish-freezer-temp.sh
```

## Components

### ds18b20-temp.py

See https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

Script to read temperatures from a DS18B20 temperature sensor connected to a
Raspberry Pi and write to STDOUT in a format suitable for the home automation 
project.

```shell
pi@niwot:~/Documents/home_automation-MQTT-sensors/DS18B20 $ ./ds18b20-temp.py
  1553183625, -6.2
pi@niwot:~/Documents/home_automation-MQTT-sensors/DS18B20 $
```

### Requirements

Enable 1 wire interface on Raspberry Pi.

* Add `dtoverlay=w1-gpio` to the end of `/boot/config.txt`.

Install `mosquitto-clients`

```shell
sudo apt install mosquitto-clients
```

### ds18b20-test.py

Test script to read sensor, report results and exit. Does not require paho-mqtt.

### Status

Working in production.

#### Obsolete

The following files are obsolete following the move to a cron job from a systemd service.

* freezer_temp.service

### TODO

* Hosts and topic are presently hard coded.
* There are no unit tests for the Python code.
