#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import paho.mqtt.client as paho   # pip install paho-mqtt
import logging
import os
import signal
import sys
import time

__author__    = 'Ben Jones <ben.jones12()gmail.com>'
__copyright__ = 'Copyright 2014 Ben Jones'
__license__   = """Eclipse Public License - v 1.0 (http://www.eclipse.org/legal/epl-v10.html)"""

# load configuration
configfile = os.getenv("MQTT2XBMCCONF", "/etc/mqtt2xbmc/mqtt2xbmc.conf")
conf = {}
try:
    execfile(configfile, conf)
except Exception, e:
    print "Cannot load %s: %s" % (configfile, str(e))
    sys.exit(2)

LOGFILE = conf['logfile']
LOGLEVEL = conf['loglevel']
LOGFORMAT = conf['logformat']

MQTT_HOST = conf['broker']
MQTT_PORT = int(conf['port'])
MQTT_LWT = conf['lwt']

# initialise logging    
logging.basicConfig(filename=LOGFILE, level=LOGLEVEL, format=LOGFORMAT)
logging.info("Starting mqtt2xbmc")
logging.info("INFO MODE")
logging.debug("DEBUG MODE")

# initialise MQTT broker connection
mqttc = paho.Client('mqtt2xbmc', clean_session=False)

# check for authentication
if conf['username'] is not None:
    mqttc.username_pw_set(conf['username'], conf['password'])

# configure the last-will-and-testament
mqttc.will_set(MQTT_LWT, payload="mqtt2xbmc", qos=0, retain=False)

def connect():
    """
    Connect to the broker
    """
    logging.debug("Attempting connection to MQTT broker %s:%d..." % (MQTT_HOST, MQTT_PORT))
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_disconnect = on_disconnect

    result = mqttc.connect(MQTT_HOST, MQTT_PORT, 60)
    if result == 0:
        mqttc.loop_forever()
    else:
        logging.info("Connection failed with error code %s. Retrying in 10s...", result)
        time.sleep(10)
        connect()
         
def disconnect(signum, frame):
    """
    Signal handler to ensure we disconnect cleanly 
    in the event of a SIGTERM or SIGINT.
    """
    logging.debug("Disconnecting from MQTT broker...")
    mqttc.loop_stop()
    mqttc.disconnect()
    logging.debug("Exiting on signal %d", signum)
    sys.exit(signum)

def notify_xbmc(xbmchost, title, message):
    command = '{"jsonrpc":"2.0","method":"GUI.ShowNotification","params":{"title":"%s","message":"%s"},"id":1}' % (title, message)
    command = command.encode('utf-8')
    url = 'http://%s/jsonrpc' % (xbmchost)
    try:
        req = urllib2.Request(url, command)
        req.add_header("Content-type", "application/json")
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        logging.error("URLError sending %s to %s: %s" % (url, xbmchost, str(e)))
    except Exception, e:
        logging.error("Error sending JSON request to %s: %s" % (xbmchost, str(e)))
  
def on_connect(mosq, userdata, result_code):
    logging.debug("Connected to MQTT broker, subscribing to topics...")
    for sub in conf['topichost'].keys():
        logging.debug("Subscribing to %s" % sub)
        mqttc.subscribe(sub, 0)

def on_message(mosq, userdata, msg):
    """
    Message received from the broker
    """
    topic = msg.topic
    payload = str(msg.payload)
    logging.debug("Message received on %s: %s" % (topic, payload))

    hosts = None
    title = "Notification"
    
    # Try to find matching settings for this topic
    for sub in conf['topichost'].keys():
        if paho.topic_matches_sub(sub, topic):
            hosts = conf['topichost'][sub]
            break

    for sub in conf['topictitle'].keys():
        if paho.topic_matches_sub(sub, topic):
            title = conf['topictitle'][sub]
            break

    for host in hosts:
        logging.debug("Sending XBMC notification to %s [%s]..." % (host, title))
        xbmchost = conf['xbmchost'][host]
        notify_xbmc(xbmchost, title, payload)

def on_disconnect(mosq, userdata, result_code):
    """
    Handle disconnections from the broker
    """
    if result_code == 0:
        logging.info("Clean disconnection")
    else:
        logging.info("Unexpected disconnection! Reconnecting in 5 seconds...")
        logging.debug("Result code: %s", result_code)
        time.sleep(5)
        connect()

# use the signal module to handle signals
signal.signal(signal.SIGTERM, disconnect)
signal.signal(signal.SIGINT, disconnect)
        
# connect to broker and start listening
connect()
