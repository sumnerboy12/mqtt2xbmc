**NOTE: this script has been superceeded by [mqttwarn](https://github.com/jpmens/mqttwarn).**
---

# mqtt2xbmc

This program subscribes to any number of MQTT topics (including wildcards) and publishes received payloads to [XBMC](http://xbmc.org/) as onscreen notification.

You associate topic branches to XBMC hosts in the configuration file (copy `mqtt2xbmc.conf.sample` to `mqtt2xbmc.conf` for use). 

See details in the config sample for how to configure this script.

## Requirements

* An MQTT broker (e.g. [Mosquitto](http://mosquitto.org))
* One or more XBMC hosts
* The Paho Python module: `pip install paho-mqtt`
