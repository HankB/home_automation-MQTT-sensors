# Acknowledgements 

## HTU21D

The original HTU21D code in this directory (slightly modified prior to
the first commit) came from https://github.com/leon-anavi/rpi-examples
and is licensed under MIT.

## MQTT

The Mosquitto library is presently used in the code. (The paho-MQTT library
was used previously but had to be built on each host whereas the Mosquitto
library is available via a Debian package.)

Present work involves a pivot to using `mosquitto_pub` to publish and having
the sensor program read the values and then write a formatted payload to stdout.
A shell script suitable for execution by cron will be provided to run the
sensor program and pipe the output to `mosquitto_pub`.

# Usage
## Requirements
* Mosquitto library

### To build
    `sudo apt install git vim libssl-dev wiringpi libmosquitto-dev libmosquitto1`
    
The sensor program itself does not need libmosquitto packages. They are only
required for the MQTT related preograms which are left here only for historic
reasons. (vim technically not required if you prefer a different editor. ;) )
    
* Enable i2c 

    `sudo raspi-config` and look for "Interfacing Options"

## Build executable

`make HTU21D_test`  # app to test HTU21D readings.

`make test_MQTT`   # app to test MQTT publishing

`make`             # build application
## Installation of binaries only

* enable i2c using `sudo raspi-config` (along with hostname, timezone, localisation etc.)
* `mkdir bin && cd bin`
* copy binary and script from build host. (`HTU21D_report temp_humidity_cron.sh`)
* edit `temp_humidity_cron` appropriately,
* install MQTT clients  and wiringpi `sudo apt install mosquitto-clients wiringpi`
## Installation as a systemd service
#### This is deprecated as the new strategy is to run via cron.
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


