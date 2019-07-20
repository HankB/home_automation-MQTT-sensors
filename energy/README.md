# Support energy monitoring

This is used to monitor the energy used by the basement freezer using a TP-Link HS-110
smart outlet. Related to this is a script that monitors temperatyre using a DS18B20
temperature sensor connected to a Raspberry Pi Zero
(`.../home_automation-MQTT-sensors/DS18B20`).

## Modules

### Requirements

Install paho-mqtt following instructions at https://www.eclipse.org/paho/clients/python/.

* paho-mqtt module as above.

    `pip install paho-mqtt`

### Status

* Reads one sample and reports reply to STDOUT.
* Parse desired info from reply.
* Publish to MQTT server

### TODO

* Update TODO list ;)
* Done - Make topic command line arguments.
* <s>Recover from dropped MQTT server connection.</s>
* Open/Close connection for each sample to send.
* Investigate switch to libmosquitto
