##################################################
##	This python program reads the values of the 
##  Raspberry PI PIN number 12. Where the PIR 
##  detector is plugged on. It the publishes to the
##  MQTT broker (rpi-ney) the value. 
##
##
##  Publish the following messages:
##
##   '/piva/pir':
##
##		The output is either 1 or 0 to define whereas
##		it detected a movement (1) or not (0).
##
##
## Author: Francesco Piva
##
##################################################

import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO


# Using board pin layout
# value change of PIR detector is 1 or 0 on PIN 12.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

##################################################
# MQTT Functions
##################################################

# Called when connection is established
def on_connect(client, userdata, flags, rc):
  print("Connected: %d" % rc)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  print("%s: %s" % (msg.topic, msg.payload))

# Create client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect("rpi-ney", 1883, 60)

# Start client event loop
client.loop_start()
##################################################


##################################################
# Main
##################################################

# Poll for pin changes
def event_stream():
  while True:
    GPIO.wait_for_edge(12, GPIO.BOTH)
    yield GPIO.input(12)

# Notify broker when pin change
for status in event_stream():
  #print("value is: %d" % status)
  if status:
    client.publish("/piva/pir", 1)
  else:
    client.publish("/piva/pir", 0)

