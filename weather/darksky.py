#!/usr/bin/python3
'''
Script to fetch current weather from darksky.net, parse it and submit to
the MQTT broker on oak.
Command line arguments
-l --location <coordinates>
-k --apikey API kep provided by accuweather
-t --test simulate with test response
-v --verbosity increase verbosity of console output

first two aguments required

Location code found at "City Search" at
https://developer.accuweather.com/accuweather-locations-api/apis

This script produces the payload on stdout which can be piped to 
`mosquitto_pub` to publish
'''
import argparse
import urllib.request
import json
import sys
import time

'''
Print verbose output to stderr. The only thing that goes to stdout
is the MQTT payload
'''
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

'''
Application logic
First parse command line arguments
'''

parser = argparse.ArgumentParser()
parser.add_argument('--location', '-l', metavar="<coordinates>",
                    nargs=1, required=True, help='specify coordinates')
parser.add_argument('--apikey', '-k', metavar="<API key>",
                    nargs=1, required=True, help='provide API key')
parser.add_argument('--test', '-t', # metavar="<test option>",
                    action='store_true', help='use canned response')
parser.add_argument("--verbosity", "-v", 
                    help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
verbose = args.verbosity

if verbose:
    eprint("coordinates", args.location[0])
    eprint("API key", args.apikey[0])
    eprint("test option", args.test)

timestamp = int(time.time())

# test code - use canned data to avoid repeated calls to the server. We get 50 calls/day on the free tier
if args.test == True:
    if verbose: eprint("use test data")
    r='{"latitude":41.866611,"longitude":-88.160051,"timezone":"America/Chicago","currently":{"time":1513630000,"summary":"Partly Cloudy","icon":"partly-cloudy-day","nearestStormDistance":19,"nearestStormBearing":215,"precipIntensity":0,"precipProbability":0,"temperature":44.28,"apparentTemperature":40.6,"dewPoint":36.68,"humidity":0.74,"pressure":1012.25,"windSpeed":6.44,"windGust":13.92,"windBearing":241,"cloudCover":0.37,"uvIndex":1,"visibility":8.19,"ozone":324.26},"offset":-6}'

else:
    if verbose: eprint("Use real server response")
    url='https://api.darksky.net/forecast/'+args.apikey[0]+'/'+args.location[0]+'?exclude=minutely,hourly,daily,alerts,flags'
    if verbose: eprint("URL:", url)
    req = urllib.request.Request(url)
    r_bytes = urllib.request.urlopen(req).read()
    r = r_bytes.decode('UTF-8')

# parse response
cont = json.loads(r)
if verbose: eprint("cont:", cont)

if verbose: eprint("\nr\n:", r)

if verbose: eprint("cont[currently][time]:", cont['currently']['time'])
if verbose: eprint("cont[currently][temperature]:", cont['currently']['temperature'])
if verbose: eprint("cont[currently][humidity]:", cont['currently']['humidity'])
if verbose: eprint("cont[currently][windBearing]:", cont['currently']['windBearing'])
if verbose: eprint("cont[currently][windSpeed]:", cont['currently']['windSpeed'])
if verbose: eprint("cont[currently][summary]:", cont['currently']['summary'])

# write values of interestweather to stdout
print(  timestamp, 
        cont['currently']['time'], 
        cont['currently']['temperature'], 
        cont['currently']['humidity']*100, 
        cont['currently']['windBearing'], 
        cont['currently']['windSpeed'],
        cont['currently']['summary'], sep=', ', end='')
sys.exit(0)
