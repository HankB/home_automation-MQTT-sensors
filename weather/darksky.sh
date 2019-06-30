#!/bin/sh

# command line arguments:  API key [host]

if [ $# -le 1 ]
then
    echo "Usage: $0 API_key location [broker_host]"
    echo "location: lattitude,longitude e.g.\"41.875574,-87.6465083\""
    exit 1
fi

key=$1
location=$2

shift; shift

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

DARKSKY_REPLY=$(darksky.py -l $location -k $key 2>>/tmp/darksky.txt)
if [ ! -z "$DARKSKY_REPLY" ]
then
    echo -n $DARKSKY_REPLY| mosquitto_pub -s -t home_automation/$HOSTNAME/darksky/drksky_weather -h $host
fi
