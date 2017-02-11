##################################################
##
## Listen to messages sent from the main controller
## agent and commands the relay on and off using
## GPIOs 11 (RESET) and 12 (SET).
##
##
## Subscribe to the following messages:
##
##   '/ctrl/led':
##
##      Sent by the controller agent. The payload
##      can be either 'start' or 'stop' to turn LEDs
##      on or off.
##
##
## Author: Antony Ducommun dit Boudry
##
##################################################

import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO


# Using board pin layout for GPIO
GPIO.setmode(GPIO.BOARD)

# Setup pin 11 for relay reset
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, False)

# Setup pin 12 for relay set
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, False)

# Turn off leds at startup
GPIO.output(11, True)
time.sleep(0.5)
GPIO.output(11, False)


# Called when connection is established
def on_connect(client, userdata, flags, rc):
    print("Connected: %d" % rc)

    # subscribe to led control events
    client.subscribe("/ctrl/led")

# Called when a message is received
def on_message(client, userdata, msg):
  if msg.topic == "/ctrl/led":
    payload = str(msg.payload, encoding='utf-8')

    # The controller ask to turn the leds on:
    # - generate a pulse on 'set' pin
    if payload == "start":
      GPIO.output(12, True)
      time.sleep(0.5)
      GPIO.output(12, False)

    # The controller ask to turn the leds off
    # - generate a pulse on 'reset' pin
    if payload == "stop":
      GPIO.output(11, True)
      time.sleep(0.5)
      GPIO.output(11, False)


# Create client instance and attach event handlers
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to mqtt broker
client.connect("rpi-ney", 1883, 60)

# Blocking client event loop
client.loop_forever()
