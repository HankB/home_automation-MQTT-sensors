# Support energy monitoring

This is used to monitor the energy used by the basement freezer using a TP-Link HS-110
smart outlet. Related to this is a script that monitors temperatyre using a DS18B20
temperature sensor connected to a Raspberry Pi Zero
(`.../home_automation-MQTT-sensors/DS18B20`).

## Usage

```text
hbarta@olive05:/mnt/home/hbarta/Programming/home_automation-MQTT-sensors/energy$ ./frmn.py -h
usage: frmn.py [-h] (-t <ip> | -n <name>) [-v] [-l LOCATION] [-i INTERVAL]

Freezer monitor v0.3

optional arguments:
  -h, --help            show this help message and exit
  -t <ip>, --target <ip>
                        Target IP Address
  -n <name>, --name <name>
                        Target host name
  -v, --verbosity       increase output verbosity
  -l LOCATION, --location LOCATION
                        subject [default "basement"]
  -i INTERVAL, --interval INTERVAL
                        interval, minutes [default 5]
hbarta@olive05:/mnt/home/hbarta/Programming/home_automation-MQTT-sensors/energy$ 
```

## Modules

### Requirements

Install paho-mqtt following instructions at https://www.eclipse.org/paho/clients/python/.

* paho-mqtt module as above.

    `pip install paho-mqtt`

## Status

* Working - publishes to oak.

## TODO

* Update TODO list ;)
* Done - Make topic command line arguments.
* <s>Recover from dropped MQTT server connection.</s>
* Open/Close connection for each sample to send.
* Investigate switch to libmosquitto
