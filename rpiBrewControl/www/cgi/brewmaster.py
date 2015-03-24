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
conn = sqlite3.connect(os.getcwd()+"/"+config['dbFile'],timeout=1)

input_data  = cgi.FieldStorage()
if input_data['func'].value == "equipSummary":
    print "Content-Type: text/html\n"

    print "<table class='table table-striped table-responsive'><tr><th>Name</th><th>ID</th><th>Temp (C)</th><th>Setpoint (C)</th><th>Status</th><th>Duty</th></tr>"
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
    for sensor in sensors:
        chartNo = chartNo + 1
        c.execute("SELECT time,tempC FROM temperatures WHERE id = '"+sensor.id+"' ORDER BY time DESC LIMIT 10")
        sensor.tempC = "--"
        colnamesTemp = [cn[0] for cn in c.description]
        rowTemp = c.fetchall()
        c.execute("SELECT time, duty, setpoint FROM duty WHERE id = '"+sensor.id+"' ORDER BY time DESC LIMIT 10")
        rowStatus = c.fetchall()
        
        if rowTemp is not None:
            #print "<div id='jsontest'>"+simplejson.dumps(rowStatus)+"</div>" 
            #print "<div id='chart"+str(chartNo)+"'></div>"
            #print "<script>"
            #print "var chart"+str(chartNo)+" = c3.generate({"
            #print "bindto: '#chart"+str(chartNo)+"',"
            #print "x: 'time'"
            #print "data: {"
            #print "rows: "
            print simplejson.dumps((rowTemp))
            #print "axis: {"
            #print "x: {"
            #print "    type: 'timeseries',"
            #print "    tick: {"
            #print "       format: '%Y-%m-%d %H:%M'"
            #print "    }"
            #print "}"
            #print "}});"
            #print "</script>"
    
    print "<p>TODO: Temperature Graphs\n"+datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')+"</p>"
