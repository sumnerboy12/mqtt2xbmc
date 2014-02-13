# mqtt2xbmc

This program subscribes to any number of MQTT topics (including wildcards) and publishes received payloads to [XBMC](http://xbmc.org/) as onscreen notification.

You associate topic branches to XBMC hosts (<ipaddress>:<port>) in the configuration file (copy `mqtt2xbmc.conf.sample` to `mqtt2xbmc.conf` for use). 

See details in the config sample for how to configure this script.

## Requirements

* An MQTT broker (e.g. [Mosquitto](http://mosquitto.org))
* One or more XBMC hosts
* The Paho Python module: `pip install paho-mqtt`

## Installation

mkdir /etc/mqtt2xbmc/
git clone git://github.com/sumnerboy12/mqtt2xbmc.git /usr/local/mqtt2xbmc/
cp /usr/local/mqtt2xbmc/mqtt2xbmc.conf.sample /etc/mqtt2xbmc/mqtt2xbmc.conf
cp /usr/local/mqtt2xbmc/mqtt2xbmc.init /etc/init.d/mqtt2xbmc
update-rc.d mqtt2xbmc defaults
cp /usr/local/mqtt2xbmc/mqtt2xbmc.default /etc/default/mqtt2xbmc

* Edit /etc/default/mqtt2xbmc and /etc/mqtt2xbmc/mqtt2xbmc.conf to suit

/etc/init.d/mqtt2xbmc start
