#!/usr/bin/env python

# Load modules
import time, os
import yaml
import sqlite3
import datetime
import cgitb; cgitb.enable()
import cgi
import os
import sys

os.chdir("../")
sys.path.append(os.getcwd())

print "Content-Type: text/html\n"
#print os.getcwd()

from dbFunctions import *
from configFunctions import *

global config
config = yaml.load(file(os.getcwd()+"/"+"config.yml"))

# Load Configuration into Sensor Classes
sensors = loadSensorConfig(config)

# Create database connection
conn = sqlite3.connect(os.getcwd()+"/"+config['dbFile'])

input_data  = cgi.FieldStorage()
if input_data['func'].value == "equipSummary":
    print "<table class='table table-striped table-responsive'><tr><th>Name</th><th>ID</th><th>Temp (C)</th><th>Setpoint (C)</th><th>Status</th><th>Duty</th></tr>"
    
    for sensor in sensors:
        print "<tr><td><strong>"+sensor.name+"</strong></td><td><small>"+sensor.id+"</small></td><td>TODO!</td><td>TODO</td><td>TODO</td><td>TODO</td></tr>"
    print "</table>"
    
else:
	print "<p>TODO: Temperature Graphs\n"+datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')+"</p>"
