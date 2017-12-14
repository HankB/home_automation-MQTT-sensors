#!/bin/sh

# command line arguments:  API key [host]

if [ $# -eq 0 ]
then
    echo "Usage: $0 API_key [broker_host]"
    exit 1
fi

key=$1

shift
echo $#

if [ $# -eq 0 ]
then
    host=localhost
else
    host=$1
fi

# ID our host
HOSTNAME=`hostname`

# add user's !/bin to PATH
PATH=${HOME}/bin:$PATH

accuweather.py -l 26289_PC -k $key -v 2>>/tmp/accuweather.txt | \
mosquitto_pub -s -t home_automation/$HOSTNAME/accuweather/weather