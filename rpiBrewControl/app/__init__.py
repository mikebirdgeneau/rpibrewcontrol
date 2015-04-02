
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
import flask.ext.restless
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import basedir

# Import Additional Python Modules
import os, time, datetime
import yaml
import datetime
import RPi.GPIO as GPIO
from subprocess import Popen, PIPE
import signal
import sys
from pushbullet import Pushbullet

# Set-up Flask Application
app = Flask(__name__)
app.config.from_object('config')

#from core import db
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# Define Models
from models import *

# Import custom functions used in this application
from app.mod_pid import pidpy as PIDController
from app.mod_gpio import *
#from app.dbFunctions import *
from app.mod_config import *
from app.mod_notify import *

# Set handler for SIGINT (Ctrl-C), needed to clear GPIO
original_sigint_handler = signal.getsignal(signal.SIGINT)
def signal_handler(signal, frame):
        print "\n---\nCleaning up GPIO..."
        GPIO.cleanup()
        print "Terminating rpiBrewControl."
        sys.exit(0)  
signal.signal(signal.SIGINT, signal_handler)

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setwarnings(True)

# Load configuration
global configYaml
configYaml = yaml.load(file("config.yml"))
secretsYaml = yaml.load(file("secrets.yml"))

# Initialize Notifications
if configYaml['usePushbullet'] == "true":
    pb = Pushbullet(secretsYaml['pushbulletAPIKey'])
    push = pb.push_note("Initializing RasPiBrew", "The Brew Control has been initialized")

# Load Configuration into Sensor Classes
sensors = loadSensorConfig(configYaml)

# Initialize GPIO
initializeGPIO(configYaml)


### Flask-Restless API ###

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Sensor, methods=['GET', 'POST', 'PATCH'],max_results_per_page=20,collection_name='sensors', exclude_columns=['readings','setpoints'])
manager.create_api(Reading, methods=['GET', 'POST'],max_results_per_page=3600,collection_name='readings', exclude_columns=['sensor'])
manager.create_api(Setpoint, methods=['GET', 'POST', 'DELETE'],max_results_per_page=100,collection_name='setpoints',exclude_columns=['sensor'])

### Application Functions ####

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
    
    # Setup variables for loop:
    temp_ma_list = []
    temp_ma = 0.0
    readyPIDcalc = False
    
    timeFromLastRecord = 0.0
    
    while (True):
    # Temperature Poll
        readytemp = False
        while parent_conn_temp.poll(): #Poll Get Temperature Process Pipe
            temp_C, sensorID, elapsed = parent_conn_temp.recv() #non blocking receive from Get Temperature Process
            # Write temperature to DB
            if temp_C != -99:
                sensor.temp_C = temp_C
                sensor.elapsed = elapsed
                #print sensor.id + ": " + "{:7.2f}".format(sensor.temp_C) + "C, Setpoint: " + "{:7.2f}".format(sensor.set_point) + "C, elapsed: " + "{:6.2f}".format(sensor.elapsed) + ", duty: " + "{:6.0f}".format(sensor.duty_cycle)+"%"
        
            
            if temp_C == -99:
                #print sensorID + ": --" + "C, elapsed: " + elapsed
                continue

            if (configYaml['tempUnits'] == 'F'):
                temp = (9.0/5.0)*temp_C + 32
            else:
                temp = temp_C
            
            temp_str = "%3.2f" % temp
            readytemp = True
            
        if readytemp == True:
            if sensor.heaterMode != 0:
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

                #calculate PID every cycle
                if (readyPIDcalc == True):
                    sensor.duty_cycle = pid.calcPID_reg4(temp_ma, sensor.set_point, True)
                    #send to heat process every cycle
                    parent_conn_heat.send([sensor.cycle_time, sensor.duty_cycle])
                    readyPIDcalc = False
                        
        while parent_conn_heat.poll(): #Poll Heat Process Pipe
                sensor.cycle_time, sensor.duty_cycle = parent_conn_heat.recv() #non blocking receive from Heat Process ")
   
        pid = PIDController.pidpy(sensor.cycle_time, sensor.Kc, sensor.Ti, sensor.Td) #init pid
        readyPIDcalc = True
        
        if(readyPIDcalc & readytemp):
            
            # Save Temperature to DB if interval record_freq is reached (avoid storing too often!)
            timeFromLastRecord = timeFromLastRecord + float(elapsed)
            if(timeFromLastRecord>=float(sensor.record_freq)):
                timeFromLastRecord = 0.0
                thisReading = Reading(sensor.id, temp_C, sensor.set_point, sensor.duty_cycle, sensor.heaterMode)
                db_session.add(thisReading)
                db_session.commit()
                db_session.close()

            # Update Sensor Record in DB
            db_session.query(Sensor).filter(Sensor.sensor_id==sensor.id).update({Sensor.tempC: temp_C, Sensor.dutyCycle: sensor.duty_cycle, Sensor.updated: datetime.datetime.utcnow()})
            db_session.commit()
            db_session.close()


# Set up second session for writing to the DB (to avoid errors!)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))


db.create_all()

# Set-up Temperature Control Process for each sensor by calling tempControlProc:
@app.before_first_request
def initialize():
    # Setup Processes: Main, Temperature, Heating
    p = current_process()
    print 'Starting:', p.name, p.pid

    
    # Add sensors to DB (from latest config)
    for sensor in sensors:
        print("Loading sensor Data for: "+sensor.id)
        # Check if sensor exists in db:
        if Sensor.query.filter_by(sensor_id=sensor.id).count() == 1:
            # Update sensor
            Sensor.query.filter_by(sensor_id=sensor.id).update(dict(
                sensor_id=sensor.id, name=sensor.name, heatPin=sensor.heatPin, 
            heaterMode = sensor.heaterMode, sensorEnabled = sensor.sensorEnabled, 
            setPoint = sensor.set_point, dutyCycle = sensor.duty_cycle, 
            alarmLL = sensor.alarmLL, alarmHH = sensor.alarmHH, 
            alarmL = sensor.alarmL, alarmH = sensor.alarmH, pidKc = sensor.Kc,
            pidTi = sensor.Ti, pidTd = sensor.Td, Ts = sensor.cycle_time,
            smoothPts = sensor.smoothPts, updated = datetime.datetime.utcnow()))
            db.session.commit()
            db.session.close()
        else:
            # Create new sensor:
            thisSensor = Sensor(sensor.id, sensor.name, sensor.heatPin, 
            sensor.heaterMode, sensor.sensorEnabled, sensor.set_point, sensor.duty_cycle, 
            sensor.alarmLL, sensor.alarmHH, sensor.alarmL, sensor.alarmH, sensor.Kc,
            sensor.Ti, sensor.Td, sensor.cycle_time, sensor.smoothPts, datetime.datetime.utcnow())
            db.session.add(thisSensor)
            db.session.commit()
            db.session.close()

        parent_conn, child_conn = Pipe()     
        p = Process(name = "tempControlProc", target=tempControlProc, args=(sensor,child_conn))
        p.start()


### Run Application ###

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('index.html')  # render a template
    #return "Hello, World!"  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

