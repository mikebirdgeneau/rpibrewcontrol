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
global config
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
def tempControlProc(sensor, proc):
    
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
    
    temp_ma_list = []
    temp_ma = 0.0
    
    readyPIDcalc = False
    while (True):
    # Temperature Poll
        readytemp = False
        while parent_conn_temp.poll(): #Poll Get Temperature Process Pipe
            temp_C, sensorID, elapsed = parent_conn_temp.recv() #non blocking receive from Get Temperature Process
            # Write temperature to DB
            if temp_C != -99:
                sensor.temp_C = temp_C
                sensor.elapsed = elapsed
                conn = sqlite3.connect(config['dbFile'])
                add_temp_reading(conn,datetime.datetime.utcnow(),sensorID,temp_C)
                conn.close()
                print sensor.id + ": " + "{:7.2f}".format(sensor.temp_C) + "C, Setpoint: " + "{:7.2f}".format(sensor.set_point) + "C, elapsed: " + sensor.elapsed + ", duty: " + "{:6.0f}".format(sensor.duty_cycle)+"%"
        
            
            if temp_C == -99:
                #print sensorID + ": --" + "C, elapsed: " + elapsed
                continue

            if (config['tempUnits'] == 'F'):
                temp = (9.0/5.0)*temp_C + 32
            else:
                temp = temp_C
            
            temp_str = "%3.2f" % temp
            readytemp = True
            
        if readytemp == True:
            if sensor.heaterEnabled == 1:
                temp_ma_list.append(temp)
                #smooth data
                temp_ma = 0.0 #moving avg init
                while (len(temp_ma_list) > sensor.smoothPts):
                    temp_ma_list.pop(0) #remove oldest elements in list

                if (len(temp_ma_list) < sensor.smoothPts):
                    for temp_pnt in temp_ma_list:
                        temp_ma += temp_pnt
                    temp_ma /= len(temp_ma_list)
                else: #len(temp_ma_list) == num_pnts_smooth
                    for temp_idx in range(sensor.smoothPts):
                        temp_ma += temp_ma_list[temp_idx]
                    temp_ma /= sensor.smoothPts

                #print "len(temp_ma_list) = %d" % len(temp_ma_list)
                #print "Num Points smooth = %d" % num_pnts_smooth
                #print "temp_ma = %.2f" % temp_ma
                #print temp_ma_list

                #calculate PID every cycle
                if (readyPIDcalc == True):
                    sensor.duty_cycle = pid.calcPID_reg4(temp_ma, sensor.set_point, True)
                    #send to heat process every cycle
                    parent_conn_heat.send([sensor.cycle_time, sensor.duty_cycle])
                    readyPIDcalc = False
                        
        while parent_conn_heat.poll(): #Poll Heat Process Pipe
                sensor.cycle_time, sensor.duty_cycle = parent_conn_heat.recv() #non blocking receive from Heat Process ")
                
                conn = sqlite3.connect(config['dbFile'])
                add_duty_reading(conn,datetime.datetime.utcnow(),sensor.id,sensor.duty_cycle,sensor.set_point)
                conn.close()
                
        pid = PIDController.pidpy(sensor.cycle_time, sensor.Kc, sensor.Ti, sensor.Td) #init pid
        readyPIDcalc = True
        

    
    # Temperature set-point as a function of time, incl. DB functions.
    
    # Temperature Control (PID)

    # Perform auto tuning (optional)?

    # Heat Poll
    
    #Trigger notifications (iPhone, etc.) for Alarms.


# Set-up Temperature Control Process for each sensor by calling tempControlProc:
for sensor in sensors:
    statusQ = Queue(2)       
    parent_conn, child_conn = Pipe()     
    p = Process(name = "tempControlProc", target=tempControlProc, args=(sensor,child_conn))
    p.start()

# Cleanup and release GPIO
print "Terminating Daemon..."
GPIO.cleanup()
