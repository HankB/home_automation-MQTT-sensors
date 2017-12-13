# Acknowledgements 

## HTU21D

The original HTU21D code in this directory (slightly modified prior to
the first commit) came from https://github.com/leon-anavi/rpi-examples
and is licensed under MIT.

## MQTT

The Mosquitto library is presently used in the code. (The paho-MQTT library
was used previously but had to be built on each host whereas the Mosquitto
library is available via a Debian package.)

# Usage
## Requirements
* Mosquitto library

    `sudo apt install git vim libssl-dev wiringpi libmosquitto-dev libmosquitto1`
    
    (vim technically not required if you prefer a different editor. ;) )
    
* Enable i2c 

    `sudo raspi-config` and look for "Interfacing Options"

## Build executable

`make HTU21D_test`  # app to test HTU21D readings.

`make test_MQTT`   # app to test MQTT publishing

`make`             # build application
## Installation as a systemd service
Modify temp_humidity.sh, temp_mon.service as needed for
* user name (pi vs. hbarta)
* location (temp_humidity.sh)
* description (temp_humidity.sh)


`chmod +x temp_humidity.sh`

`cp temp_humidity.sh /home/hbarta/bin/temp_humidity.sh`
   or
`cp temp_humidity.sh /home/pi/bin/temp_humidity.sh`

`mkdir /home/hbarta/temp_humidity`
   or
`mkdir /home/pi/temp_humidity`

`cp HTU21D_publish /home/hbarta/bin`
   or
`cp HTU21D_publish /home/pi/bin`

`sudo cp temp_mon.service /etc/systemd/system/`

`sudo systemctl start temp_mon`

`systemctl status temp_mon.service`

and should result in

* temp_mon.service
    Loaded: loaded (/etc/systemd/system/temp_mon.service; disabled; vendor preset: enabled)
    Active: active (running) since Mon 2017-11-20 15:14:01 CST; 6s ago
    Main PID: 1878 (temp_humidity.s)
    CGroup: /system.slice/temp_mon.service
            |-1878 /bin/sh /home/hbarta/bin/temp_humidity.sh
            `-1879 /home/hbarta/bin/HTU21D_publish -i 1 -l dining_room -d temp_humidity

    Nov 20 15:14:01 polana systemd[1]: Started temp_mon.service.

If the problem with i2c enable not surviving a reboot is solved, the following
line should enable the service at boot.

`sudo systemctl enable temp_mon`


