#!/bin/sh
# meant to be run fron cron
# */5 * * * * /home/pi/bin/publish-freezer-temp.sh
/home/pi/bin/ds18b20-temp.py | sed -e "s/  //"|tr -d '\n'| /usr/bin/mosquitto_pub -s -t "home_automation/niwot/basement/freezer_temp" -h oak
