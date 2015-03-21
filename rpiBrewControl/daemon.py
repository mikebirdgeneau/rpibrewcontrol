# Backend Daemon to Record Temperatures to SQLite DB


# Load modules
import os
import yaml
import sqlite3
import datetime
import RPi.GPIO as GPIO
from subprocess import Popen, PIPE
import signal
import sys
from pushbullet import Pushbullet

# Import functions from other files in this project
from pid import pidpy as PIDController
from gpioFunctions import *
from dbFunctions import *
from configFunctions import *
from notificationFunctions import *

# Set handler for SIGINT (Ctrl-C)
signal.signal(signal.SIGINT, signal_handler)

# Load configuration
config = yaml.load(file("config.yml"))
secrets = yaml.load(file("secrets.yml"))

# Initialize Notifications
if config['usePushbullet'] == "true":
    pb = Pushbullet(secrets['pushbulletAPIKey'])
    push = pb.push_note("Initializing RasPiBrew", "The Brew Control has been initialized")

# Load Configuration into Sensor Classes
sensors = loadSensorConfig(config)

# Create database connection
conn = sqlite3.connect(config['dbFile'])

# Initialize GPIO
initializeGPIO(config)
       
       
# Poll Temperature Sensors
print datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
for sensor in sensors:
    curTemp = tempData1Wire(sensor.id)
    if(add_temp_reading(conn,datetime.datetime.utcnow(),sensor.id,curTemp)==0):
        print sensor.id + ": " + "{:10.3f}".format(curTemp) + "C"

# Read Current Temperatures, break into subprocesses / threads?
# Temperature set-point as a function of time, incl. DB functions.
# PID control loop
# Perform auto tuning (optional)?

#Trigger notifications (iPhone, etc.) for Alarms.

# Cleanup and release GPIO
print "Terminating Daemon..."
GPIO.cleanup()
