import paho.mqtt.client as mqtt
import time
import quick2wire.i2c as i2c

address = 0x40

with i2c.I2CMaster() as bus:
  bus.transaction(i2c.writing(address, [0xF3]))
  time.sleep(0.05)
  buffer = bus.transaction(i2c.reading(address, 3))[0]
  print(buffer)
  value = buffer[0] << 8 | buffer[1]
  print(value)
  temp = 175.72 * value / 65536 - 46.85

  bus.transaction(i2c.writing(address, [0xF5]))
  time.sleep(0.05)
  buffer = bus.transaction(i2c.reading(address, 3))[0]
  print(buffer)
  value = buffer[0] << 8 | buffer[1]
  print(value)
  temp = 125 * value / 65536 - 6
  print(temp)

