# home_automation-MQTT-sensors
##### `ssh://git@oak:10022/HankB/home_automation-MQTT-sensors.git`

Various scripts and programs to read sensors and publish to the MQTT server
on oak. Many of these are intended to execute on a Raspberry Pi and read
sensors connected to GPIO pins. Others execute on any convenient Linux host.

## Modules

* DS18B20 - Read temperature from this sensor and publish. Read power usage from HS110 and publish. Used to monitor basement freezer operation.
* HTU21D - Read temperature from HTU21D sensor and publish or write to standard output (publish using `mosquitto_pub`)
* weather - Fetch weather from an Internet source in order to compare to outdoor temperature and humidity readings.
