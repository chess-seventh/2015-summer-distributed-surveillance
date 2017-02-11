##################################################
##	This python program reads the values of the i2c 
##  probe and converts them for human understanding
##	Celsius degrees and % for humidity. 
##  Then publishes the 'messages/values' for a future
##	reading from the MQTT broker (rpi-ney)
##
##
##  Publish the following messages:
##
##   '/piva/temperature':
##
##		The temperature is published in a string
##		and the format is in floating point with
##		2 decimals.
##
##   '/piva/humidity':
##
##		The humidity is published in a string
##		and the format is in floating point with
##		2 decimals.
##
## Author: Francesco Piva
##
##################################################

import paho.mqtt.client as mqtt
import time
import quick2wire.i2c as i2c


# HTU21DF  i2c parameters
# all addresses are referenced on the documentation of the i2c temp + humidity sensor.
I2C_ADDR = 0x40
I2C_REG_START_TEMP = 0xf3
I2C_REG_START_HUMIDITY = 0xf5

##########################################################
# MQTT Functions
##########################################################

# Called when connection is established
def on_connect(client, userdata, flags, rc):
  print("Connected: %d" % rc)

# Called when a message is received
def on_message(client, userdata, msg):
  print("%s: %s" % (msg.topic, msg.payload))

# Create client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect("rpi-ney", 1883, 60)
client.loop_start()


#######################################################
# Main 
#######################################################

# using 'with' in order to make sure to close it.
with i2c.I2CMaster() as bus:

	#MAIN LOOP Start.
  while True:
    # Read raw temperature from the HTU21DF sensor
	# at specified address in the documentation
    bus.transaction(i2c.writing(I2C_ADDR, [I2C_REG_START_TEMP]))
    # we wait for 50ms between each measure because of the specification of the probe.
    time.sleep(0.05)
	
    buffer = bus.transaction(i2c.reading(I2C_ADDR, 3))[0]
    value = buffer[0] << 8 | buffer[1]

    # convert temperature in degree celcius
    temperature = 175.72 * value / 65536 - 46.85

    # Read raw humidity from the HTU21DF sensor
	# at specified address in the documentation
    bus.transaction(i2c.writing(I2C_ADDR, [I2C_REG_START_HUMIDITY]))
	# we wait for 50ms between each measure because of the specification of the probe.
    time.sleep(0.05)
	
    buffer = bus.transaction(i2c.reading(I2C_ADDR, 3))[0]
    value = buffer[0] << 8 | buffer[1]

    # convert humidity in percentage
    humidity = 125 * value / 65536 - 6

    # broadcast measurements
    client.publish("/piva/temperature", "%.02f" % temperature)
    client.publish("/piva/humidity", "%.02f" % humidity)

    # wait 10 seconds then repeat.
    time.sleep(10)
