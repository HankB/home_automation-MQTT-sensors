# fetch weather conditions 
Publish to an MQTT broker. These scripts will exercise a different model
than other efforts. The code that produces the readings will write them to
stdout and the program `mosquitto_pub` will be used to publish to the MQTT
broker.

## Requirements
* API keys from the various providers
* Mosquitto client programs

    `apt install -y mosquitto-clients`

## Status
OpenWeatherClient variant set aside for the moment. It seems to update too infrequently.
