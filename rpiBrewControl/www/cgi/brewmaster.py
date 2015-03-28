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
import simplejson

os.chdir("../")
sys.path.append(os.getcwd())

#print os.getcwd()

from dbFunctions import *
from configFunctions import *

global config
config = yaml.load(file(os.getcwd()+"/"+"config.yml"))

# Load Configuration into Sensor Classes
sensors = loadSensorConfig(config)

# Create database connection
conn = sqlite3.connect(os.getcwd()+"/"+config['dbFile'])
conn.execute("PRAGMA busy_timeout = 30000")

input_data  = cgi.FieldStorage()
if input_data['func'].value == "equipSummary":
    print "Content-Type: text/html\n"

    print "<table class='table table-striped table-responsive'><tr><th>Name</th><th>ID</th><th>Temp (C)</th><th>Setpoint (C)</th><th>Status</th><th>Duty (%)</th></tr>"
    c = conn.cursor()
    for sensor in sensors:
        c.execute("SELECT * FROM temperatures WHERE id = '"+sensor.id+"' ORDER BY time DESC LIMIT 1")
        sensor.tempC = "--"
        rowTemp = c.fetchone()
        c.execute("SELECT * FROM duty WHERE id = '"+sensor.id+"' ORDER BY time DESC LIMIT 1")
        rowStatus = c.fetchone()
        if rowTemp is not None:
            if isinstance(rowTemp[2], float):
                sensor.tempC = "{:10.2f}".format(rowTemp[2])
        if rowStatus is not None:
            if isinstance(rowStatus[2], float):
                sensor.duty = "{:10.0f}".format(rowStatus[2])
            if isinstance(rowStatus[3], float):
                sensor.setpoint = "{:10.2f}".format(rowStatus[3])
                
        print "<tr><td><strong>"+sensor.name+"</strong></td><td><small>"+sensor.id+"</small></td><td>"+sensor.tempC+"</td><td>"+sensor.setpoint+"</td><td>TODO</td><td>"+sensor.duty+"</td></tr>"
    
    print "</table>"
    
else:
    print "Content-Type: application/json\n"
    c = conn.cursor()
    chartNo = 0
    sensor = sensors[int(input_data['sensnum'].value)]
    chartNo = chartNo + 1
    c.execute("SELECT time,tempC FROM temperatures WHERE id = '"+sensor.id+"' ORDER BY time DESC LIMIT 10")

    r = [dict((c.description[i][0], value) \
               for i, value in enumerate(row)) for row in c.fetchall()]

    #result = []
    #columns = tuple( [d[0].decode('utf8') for d in c.description] )
    #for row in c:
    #    result.append(row)
    #rows = c.fetchall()
    print simplejson.dumps(r)
    
    #print simplejson.dumps(result)
    #print "<p>TODO: Temperature Graphs\n"+datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')+"</p>"
