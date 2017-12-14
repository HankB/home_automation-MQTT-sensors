#!/usr/bin/python3
'''
Script to fetch current weather from Accuweather, parse it and submit to
the MQTT broker on oak.
Command line arguments
-l --location <location code>
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
parser.add_argument('--location', '-l', metavar="<location code>",
                    nargs=1, required=True, help='specify location code')
parser.add_argument('--apikey', '-k', metavar="<API key>",
                    nargs=1, required=True, help='broker host name')
parser.add_argument('--test', '-t', # metavar="<test option>",
                    action='store_true', help='use canned response')
parser.add_argument("--verbosity", "-v", 
                    help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
verbose = args.verbosity

if verbose:
    eprint("location code", args.location[0])
    eprint("API key", args.apikey[0])
    eprint("test option", args.test)

timestamp = int(time.time())

# test code - use canned data to avoid repeated calls to the server. We get 50 calls/day on the free tier
if args.test == True:
    if verbose: eprint("use test data")
    r='[ { "LocalObservationDateTime": "2017-12-11T21:10:00-06:00", "EpochTime": 1513048200, "WeatherText": "Cloudy", "WeatherIcon": 7, "IsDayTime": false, "Temperature": { "Metric": { "Value": 0, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 32, "Unit": "F", "UnitType": 18 } }, "RealFeelTemperature": { "Metric": { "Value": -8.9, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 16, "Unit": "F", "UnitType": 18 } }, "RealFeelTemperatureShade": { "Metric": { "Value": -8.9, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 16, "Unit": "F", "UnitType": 18 } }, "RelativeHumidity": 88, "DewPoint": { "Metric": { "Value": -1.7, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 29, "Unit": "F", "UnitType": 18 } }, "Wind": { "Direction": { "Degrees": 338, "Localized": "NNW", "English": "NNW" }, "Speed": { "Metric": { "Value": 29.6, "Unit": "km/h", "UnitType": 7 }, "Imperial": { "Value": 18.4, "Unit": "mi/h", "UnitType": 9 } } }, "WindGust": { "Speed": { "Metric": { "Value": 29.6, "Unit": "km/h", "UnitType": 7 }, "Imperial": { "Value": 18.4, "Unit": "mi/h", "UnitType": 9 } } }, "UVIndex": 0, "UVIndexText": "Low", "Visibility": { "Metric": { "Value": 8, "Unit": "km", "UnitType": 6 }, "Imperial": { "Value": 5, "Unit": "mi", "UnitType": 2 } }, "ObstructionsToVisibility": "F", "CloudCover": 100, "Ceiling": { "Metric": { "Value": 335, "Unit": "m", "UnitType": 5 }, "Imperial": { "Value": 1100, "Unit": "ft", "UnitType": 0 } }, "Pressure": { "Metric": { "Value": 1011.2, "Unit": "mb", "UnitType": 14 }, "Imperial": { "Value": 29.86, "Unit": "inHg", "UnitType": 12 } }, "PressureTendency": { "LocalizedText": "Rising", "Code": "R" }, "Past24HourTemperatureDeparture": { "Metric": { "Value": 4.4, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 8, "Unit": "F", "UnitType": 18 } }, "ApparentTemperature": { "Metric": { "Value": 0, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 32, "Unit": "F", "UnitType": 18 } }, "WindChillTemperature": { "Metric": { "Value": -6.1, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 21, "Unit": "F", "UnitType": 18 } }, "WetBulbTemperature": { "Metric": { "Value": -0.6, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 31, "Unit": "F", "UnitType": 18 } }, "Precip1hr": { "Metric": { "Value": 0, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0, "Unit": "in", "UnitType": 1 } }, "PrecipitationSummary": { "Precipitation": { "Metric": { "Value": 0, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.01, "Unit": "in", "UnitType": 1 } }, "PastHour": { "Metric": { "Value": 0, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0, "Unit": "in", "UnitType": 1 } }, "Past3Hours": { "Metric": { "Value": 0, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.01, "Unit": "in", "UnitType": 1 } }, "Past6Hours": { "Metric": { "Value": 2, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.08, "Unit": "in", "UnitType": 1 } }, "Past9Hours": { "Metric": { "Value": 2, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.08, "Unit": "in", "UnitType": 1 } }, "Past12Hours": { "Metric": { "Value": 2, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.08, "Unit": "in", "UnitType": 1 } }, "Past18Hours": { "Metric": { "Value": 3, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.13, "Unit": "in", "UnitType": 1 } }, "Past24Hours": { "Metric": { "Value": 3, "Unit": "mm", "UnitType": 3 }, "Imperial": { "Value": 0.13, "Unit": "in", "UnitType": 1 } } }, "TemperatureSummary": { "Past6HourRange": { "Minimum": { "Metric": { "Value": 0, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 32, "Unit": "F", "UnitType": 18 } }, "Maximum": { "Metric": { "Value": 3.2, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 38, "Unit": "F", "UnitType": 18 } } }, "Past12HourRange": { "Minimum": { "Metric": { "Value": -1.7, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 29, "Unit": "F", "UnitType": 18 } }, "Maximum": { "Metric": { "Value": 4.4, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 40, "Unit": "F", "UnitType": 18 } } }, "Past24HourRange": { "Minimum": { "Metric": { "Value": -8.3, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 17, "Unit": "F", "UnitType": 18 } }, "Maximum": { "Metric": { "Value": 4.4, "Unit": "C", "UnitType": 17 }, "Imperial": { "Value": 40, "Unit": "F", "UnitType": 18 } } } }, "MobileLink": "http://m.accuweather.com/en/us/winfield-il/60190/current-weather/2256467?lang=en-us", "Link": "http://www.accuweather.com/en/us/winfield-il/60190/current-weather/2256467?lang=en-us" } ]'

else:
    if verbose: eprint("Use real server response")
    url='http://dataservice.accuweather.com/currentconditions/v1/'+args.location[0]+'?apikey='+args.apikey[0]+'&details=true'
    if verbose: eprint("URL:", url)
    req = urllib.request.Request(url)
    r_bytes = urllib.request.urlopen(req).read()
    r = r_bytes.decode('UTF-8')

# parse response
cont = json.loads(r[1:-1])
if verbose: eprint("cont:", cont)

if verbose: eprint("\nr\n:", r)

if verbose: eprint("cont[Temperature][Imperial]['Value']:", cont['Temperature']['Imperial']['Value'])
if verbose: eprint("cont[RelativeHumidity]:", cont['RelativeHumidity'])
if verbose: eprint("cont[Wind][Direction][Degrees]:", cont['Wind']['Direction']['Degrees'])
if verbose: eprint("cont[Wind][Speed][Imperial][Value]:", cont['Wind']['Speed']['Imperial']['Value'])
if verbose: eprint("cont[EpochTime]:", cont['EpochTime'])
if verbose: eprint("cont[WeatherText]:", cont['WeatherText'])

# write values of interestweather to stdout
print(  timestamp, 
        cont['EpochTime'], 
        cont['Temperature']['Imperial']['Value'], 
        cont['RelativeHumidity'], 
        cont['Wind']['Direction']['Degrees'], 
        cont['Wind']['Speed']['Imperial']['Value'],
        cont['WeatherText'], sep=', ')
sys.exit(0)
