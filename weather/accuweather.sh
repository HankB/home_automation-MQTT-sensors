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

HOSTNAME=`hostname`

echo host $host
echo API key $key
echo $HOSTNAME

/home/hbarta/bin/accuweather.py -l 26289_PC -k $key -t -v 2>>/tmp/accuweather.txt | \
mosquitto_pub -s -t home_automation/$HOSTNAME/accuweather/weather