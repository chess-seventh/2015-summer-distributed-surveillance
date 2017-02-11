##################################################
##
## Listen to '/ctrl/video' messages sent from the
## main controller agent and commands the motion
## daemon to detect movement or not using RPC over
## http.
##
##
## Subscribe to the following messages:
##
##   '/ctrl/video':
##
##      Sent by the controller agent. The payload
##      can be either 'start' or 'stop' to turn
##      movement detection in the video on or off.
##
##
## Author: Antony Ducommun dit Boudry
##
##################################################

import paho.mqtt.client as mqtt
import time
import http.client


# Called when connection is established
def on_connect(client, userdata, flags, rc):
    print("Connected: %d" % rc)

    # subscribe to video control events
    client.subscribe("/ctrl/video")

# Called when a message is received
def on_message(client, userdata, msg):
  if msg.topic == "/ctrl/video":
    payload = str(msg.payload, encoding='utf-8')

    # The controller ask to turn the movement detection on:
    # - call motion rpc
    if payload == "start":
      client2 = http.client.HTTPConnection('localhost', 8080, timeout=10)
      client2.request('GET', '/0/detection/start')
      response = client2.getresponse()

      # if it fails, notify broker with an error message
      if response.status != 200:
        client.publish("/motion/error", "cannot start")

    # The controller ask to turn the movement detection off:
    # - call motion rpc
    if payload == "stop":
      client2 = http.client.HTTPConnection('localhost', 8080, timeout=10)
      client2.request('GET', '/0/detection/pause')
      response = client2.getresponse()

      # if it fails, notify broker with an error message
      if response.status != 200:
        client.publish("/motion/error", "cannot stop")


# Create client instance and attach event handlers
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to mqtt broker
client.connect("rpi-ney", 1883, 60)

# Blocking client event loop
client.loop_forever()
