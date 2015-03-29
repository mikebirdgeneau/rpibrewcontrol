### Import Modules ###

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless

# Import Python Modules
import time, os
import yaml
import datetime
import RPi.GPIO as GPIO
from subprocess import Popen, PIPE
import signal
import sys
from pushbullet import Pushbullet

# Import custom functions used in this application
from pid import pidpy as PIDController
from gpioFunctions import *
from dbFunctions import *
from configFunctions import *
from notificationFunctions import *

### Configuration ###

# Set-up Flask Application Settings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://brewPi:brewPi@localhost/brewPi'
db = SQLAlchemy(app)

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

# Initialize GPIO
initializeGPIO(config)

### Define Data Model ###

# Moved tp app/models.py

# Create the database tables.
db.create_all()

### Flask-Restless API ###

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Sensor, methods=['GET', 'POST', 'PATCH'])
manager.create_api(Reading, methods=['GET', 'POST'])
manager.create_api(Setpoint, methods=['GET', 'POST', 'DELETE'])


### Application Functions ####


### Run Application ###

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# start the server with the 'run()' method
#if __name__ == '__main__':
#    app.run(debug=True,host='0.0.0.0', port=8080)