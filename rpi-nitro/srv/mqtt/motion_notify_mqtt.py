##################################################
##
## Called by motion daemon when it detects movement
## on the camera. It notifies the event to the
## broker.
##
##
## Publish the following messages:
##
##   '/motion/on_event_start':
##
##      A new event has been detected by motion. The
##      payload is the event unique identifier.
##
##   '/motion/on_event_end':
##
##      An event previously detected by motion is now
##      finished. The payload is the event unique
##      identifier.
##
##   '/motion/on_movie_start':
##
##      A new video is being recorded by motion. The
##      payload is the video unique identifier.
##
##   '/motion/on_movie_end':
##
##      A video recorded by motion is complete. The
##      payload is the video unique identifier.
##
##
## Author: Antony Ducommun dit Boudry
##
##################################################

import paho.mqtt.client as mqtt
import time
import sys


# Called when connection is established
def on_connect(client, userdata, flags, rc):
  print("Connected: %d" % rc)

# Called when a message is received
def on_message(client, userdata, msg):
  print("%s: %s" % (msg.topic, msg.payload))

# Create client instance and attach event handlers
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to mqtt broker
client.connect("rpi-ney", 1883, 60)

# Start client loop
client.loop_start()

# Notify event to broker
client.publish("/motion/%s" % sys.argv[1], sys.argv[2])

# Gracefully stop client loop
client.loop_stop()
