#!/bin/sh

# command line arguments: description [host]
# topic example "home_automation/haut/dining_room/temp_humidity"

if [ $# -eq 0 ]
then
    echo "Usage: $0 description [broker_host]"
    exit 1
fi

description=$1

shift

if [ $# -eq 0 ]
then
    host=localhost      #default
else
    host=$1
fi

# ID our host
HOSTNAME=`hostname`

# add user's !/bin to PATH
PATH=${HOME}/bin:$PATH

HTU21D_report 2>/tmp/temp_humidity_cron.txt | \
mosquitto_pub -s -t "home_automation/$HOSTNAME/$description/temp_humidity" -h $host
