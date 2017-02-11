##################################################
##
## Setup TSL2591 sensor over I2C and make measurements
## every 10 seconds.
##
## Publish the following message:
##
##   '/nitro/luminosity':
##
##      A measurement was done. The payload is the
##      raw luminosity value as integer.
##
##
## Authors: Antony Ducommun dit Boudry
##          Francesco Piva
##
##################################################

import paho.mqtt.client as mqtt
import time
import quick2wire.i2c as i2c


# TSL2591 i2c parameters
# all addresses are referenced on the documentation of the i2c sensor.
I2C_ADDR = 0x29
I2C_REG_ENABLE = 0x00
I2C_REG_CONFIG = 0x01
I2C_REG_CHAN0_LOW = 0x14
I2C_REG_CHAN1_LOW = 0x0E
I2C_REG_STATUS = 0x13

I2C_CMD_BIT = 0x80
I2C_CMD_WORDBIT = 0x20
I2C_CMD_POWERON = 0x03
I2C_CMD_POWEROFF = 0x00

I2C_TIMING_100MS = 0x00
I2C_TIMING_200MS = 0x01
I2C_TIMING_300MS = 0x02

I2C_GAIN_LOW = 0x00
I2C_GAIN_MEDIUM = 0x01
I2C_GAIN_HIGH = 0x10
I2C_GAIN_MAXIMUM = 0x11


# ##########################################################
# # MQTT Functions
# ##########################################################

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

with i2c.I2CMaster(1) as bus:
  while True:
    # start measurement
    bus.transaction(
      i2c.writing(I2C_ADDR, [I2C_CMD_BIT | I2C_REG_CONFIG, I2C_TIMING_100MS | I2C_GAIN_MAXIMUM]),
      i2c.writing(I2C_ADDR, [I2C_CMD_BIT | I2C_REG_ENABLE, I2C_CMD_POWERON])
    )

    # wait for measurement completion
    time.sleep(0.100)
    while True:
      buffer = bus.transaction(
        i2c.writing(I2C_ADDR, [I2C_CMD_BIT | I2C_REG_STATUS]),
        i2c.reading(I2C_ADDR, 1)
      )[0]
      if buffer == b'1':
        break

    # read measurement
    buffer = bus.transaction(
      i2c.writing(I2C_ADDR, [I2C_CMD_BIT | I2C_CMD_WORDBIT | I2C_REG_CHAN0_LOW]),
      i2c.reading(I2C_ADDR, 4)
    )[0]

    chan0 = buffer[0] | buffer[1] << 8
    chan1 = buffer[2] | buffer[3] << 8

    # notify visible light measurement
    client.publish("/nitro/luminosity", chan0)

    # wait 10 seconds
    time.sleep(10)
