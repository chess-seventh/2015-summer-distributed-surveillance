import paho.mqtt.client as mqtt
import mysql.connector as mysql
import time
import sys

# List of constant
CONST_PIR = "/piva/pir"
COMMIT = ("COMMIT")
#MOTION_START = "/motion/on_event_start"
#MOTION_STOP = "/motion/on_event_end"
MOVIE_START = "/motion/on_movie_start"
MOVIE_STOP = "/motion/on_movie_end"
CONST_TEMP = "/piva/temperature"
CONST_HUM = "/piva/humidity"
CONST_LUM = "/nitro/luminosity"

# connect to database (credentials for connection inside)
def db_connect():
  con = mysql.connect(user='root', password='', host='localhost', database='video_system')
  return con
# Saving change indo database
def db_commit(cursor):
  cursor.execute(COMMIT)
  cursor.close()
# Inserting values into database
def db_insert(con , query):
  cursor = con.cursor()
  cursor.execute(query)
  db_commit(cursor)
# Updating values into database
def db_update(con , query):
  cursor = con.cursor()
  cursor.execute(query)
  db_commit(cursor)
# Closing connection
def db_close(con):
  con.close()
# Called when connection is established
def on_connect(client, userdata, flags, rc):
  print("Connected with result code %d" % rc)
  # TODO: subscribe to events if necessary
  client.subscribe(CONST_PIR)
  #client.subscribe(MOTION_START) client.subscribe(MOTION_STOP)
  client.subscribe(MOVIE_START)
  client.subscribe(MOVIE_STOP)
  client.subscribe(CONST_TEMP)
  client.subscribe(CONST_HUM)
  client.subscribe(CONST_LUM)
# Called when a message is received
def on_message(client, userdata, msg):
  # Called when temperature message is received
  def on_ctrl_temp(payload):
    try:
      con = db_connect()
      query = ("INSERT INTO temperature_events (id , device_id , created_at , value) VALUES (NULL , 1 , now() , %f )"%(float(payload)))
      db_insert(con , query)
    except mysql.Error as e:
      print("Error %d: %s" % (e.args[0], e.args[1]))
      sys.exit(1)
    finally:
      if con:
        db_close(con)
  # Called when humidity message is received
  def on_ctrl_hum(payload):
    try:
      con = db_connect()
      query = ("INSERT INTO humidity_events (id , device_id , created_at , value) VALUES (NULL , 1 , now() , %f )"%(float(payload)))
      db_insert(con , query)
    except mysql.Error as e:
      print("Error %d: %s" % (e.args[0], e.args[1]))
      sys.exit(1)
    finally:
      if con:
        db_close(con)
  # Called when luminosity message is received
  def on_ctrl_lum(payload):
    try:
      con = db_connect()
      query = ("INSERT INTO luminosity_events (id , device_id , created_at , value) VALUES (NULL , 0 , now() , %f )"%(float(payload)))
      db_insert(con , query)
    except mysql.Error as e:
      print("Error %d: %s" % (e.args[0], e.args[1]))
      sys.exit(1)
    finally:
      if con:
        db_close(con)
  # Called when pir message is received
  def on_ctrl_pir(payload):
    if payload == "1":
      try:
        con = db_connect()
        query = ("INSERT INTO pir_events (id , device_id , created_at , value) VALUES (NULL , 1 , now() , 1)")
        db_insert(con , query)
      except mysql.Error as e:
          print("Error %d: %s" % (e.args[0], e.args[1]))
          sys.exit(1)
      finally:
        if con:
          db_close(con)
    elif payload == "0":
      try:
        con = db_connect()
        query = ("INSERT INTO pir_events (id , device_id , created_at , value) VALUES (NULL , 1 , now() , 0)")
        db_insert(con , query)
      except mysql.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(1)
      finally:
        if con:
          db_close(con)
  # Called when movie start message is received
  def on_movie_start(payload):
    try:
      con = db_connect()
      query = ("INSERT INTO video_events (id , device_id , created_at , stopped_at , video_key) VALUES (NULL , 0 , now() , NULL , \"" + payload + "\")")
      db_insert(con , query)
    except mysql.Error as e:
      print("Error %d: %s" % (e.args[0], e.args[1]))
      sys.exit(1)
    finally:
      if con:
        db_close(con)
  # Called when movie stop message is received
  def on_movie_stop(payload):
    try:
      con = db_connect()
      query = ("UPDATE video_events SET stopped_at = now() where video_key = \"" + payload + "\"")
      db_insert(con , query)
    except mysql.Error as e:
      print("Error %d: %s" % (e.args[0], e.args[1]))
      sys.exit(1)
    finally:
      if con:
        db_close(con)
  message = msg.topic
  payload = str(msg.payload , "utf-8")
  if CONST_PIR == message:
    on_ctrl_pir(payload)
  #elif CONST_MOTION == message:
  #  on_ctrl_video(payload) elif MOTION_START == message: on_motion_start(payload) elif MOTION_STOP == message: on_motion_stop(payload)
  elif MOVIE_START == message:
    on_movie_start(payload)
  elif MOVIE_STOP == message:
    on_movie_stop(payload)
  elif CONST_TEMP == message:
    on_ctrl_temp(payload)
  elif CONST_HUM == message:
    on_ctrl_hum(payload)
  elif CONST_LUM == message:
    on_ctrl_lum(payload)
# Create client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# Connect to mqtt broker
client.connect("rpi-ney", 1883, 60)
# Block here:
client.loop_forever()