import paho.mqtt.client as mqtt
import sys
import time

# Const
CONST_LUM = "/nitro/luminosity"
CONST_PIR = "/piva/pir"
MOVIE_START = "/motion/on_movie_start"
MOVIE_STOP = "/motion/on_movie_end"

# List of global
lastLuminosity = 0
ledState = False
ledStartTime = None
motionDetected = False


# Called when connection is established
def on_connect(client, userdata, flags, rc):
  print("Connected with result code %d" % rc)

  client.subscribe(CONST_PIR)
  client.subscribe(CONST_LUM)
  client.subscribe(MOVIE_START)
  client.subscribe(MOVIE_STOP)


# Called when a message is received
def on_message(client, userdata, msg):
  def on_ctrl_lum(payload):
    global lastLuminosity
    global ledState
    global motionDetected

    lastLuminosity = float(payload)
    if lastLuminosity < 500 and motionDetected and not ledState:
      client.publish("/ctrl/led" , "start")
      ledState = True
    if lastLuminosity >= 500 and not motionDetected and ledState:
      client.publish("/ctrl/video" , "stop")
      client.publish("/ctrl/led" , "stop")
      time.sleep(1)
      client.publish("/ctrl/video" , "start")
      ledState = False

  # Called when pir message is received
  def on_ctrl_pir(payload):
    global lastLuminosity
    global ledState
    global ledStartTime

    if payload == "1" and lastLuminosity < 500 and not ledState:
      client.publish("/ctrl/led" , "start")
      ledState = True
      ledStartTime = time.time()

  # Called when movie start message is received
  def on_movie_start(payload):
    global lastLuminosity
    global ledState
    global motionDetected

    if lastLuminosity < 500 and not ledState:
      client.publish("/ctrl/led" , "start")
      ledState = True
    motionDetected = True

  # Called when movie stop message is received
  def on_movie_stop(payload):
    global ledState
    global motionDetected

    if ledState:
      client.publish("/ctrl/video" , "stop")
      client.publish("/ctrl/led" , "stop")
      time.sleep(1)
      client.publish("/ctrl/video" , "start")
      ledState = False
    motionDetected = False

  message = msg.topic
  payload = str(msg.payload , "utf-8")
  if CONST_LUM == message:
    on_ctrl_lum(payload)
  if CONST_PIR == message:
    on_ctrl_pir(payload)
  if MOVIE_START == message:
    on_movie_start(payload)
  if MOVIE_STOP == message:
    on_movie_stop(payload)


# Create client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# Connect to mqtt broker
client.connect("rpi-ney", 1883, 60)

# Loop for the timeout when pir is detecting movement but camera isn't
client.loop_start()
while True:
  if ledStartTime and (time.time() - ledStartTime) > 60:
    if ledState and not motionDetected:
      client.publish("/ctrl/video" , "stop")
      client.publish("/ctrl/led" , "stop")
      time.sleep(1)
      client.publish("/ctrl/video" , "start")
      ledState = False
    ledStartTime = None
  time.sleep(1)
