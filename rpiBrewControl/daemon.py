# Backend Daemon to Record Temperatures to SQLite DB


# Load modules
import time, os
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
       
       
# Setup Processes: Main, Temperature, Heating
p = current_process()
print 'Starting:', p.name, p.pid

# Main Temperature Control Process
def tempControlProc(sensor):
    
    #Pipe to communicate with "Get Temperature Process"
    parent_conn_temp, child_conn_temp = Pipe()       
    ptemp = Process(name = "gettempProc", target=gettempProc, args=(child_conn_temp, sensor))
    ptemp.daemon = True
    ptemp.start() 
    
    #Pipe to communicate with "Heat Process"
    parent_conn_heat, child_conn_heat = Pipe()
    pheat = Process(name = "heatProcGPIO", target=heatProcGPIO, args=(child_conn_heat,sensor))
    pheat.daemon = True
    pheat.start() 
    
    while (True):
    # Temperature Poll
        readytemp = False
        while parent_conn_temp.poll(): #Poll Get Temperature Process Pipe
            temp_C, sensorID, elapsed = parent_conn_temp.recv() #non blocking receive from Get Temperature Process
            print sensorID + ": " + "{:10.3f}".format(temp_C) + "C, elapsed:" + elapsed
    
    # Temperature Control (PID)
    
    # Heat Poll

# Set-up Temperature Control Process for each sensor:
for sensor in sensors:
    tempControlProc(sensor)





# Temperature set-point as a function of time, incl. DB functions.
# PID control loop
# Perform auto tuning (optional)?

#Trigger notifications (iPhone, etc.) for Alarms.

# Cleanup and release GPIO
print "Terminating Daemon..."
GPIO.cleanup()
