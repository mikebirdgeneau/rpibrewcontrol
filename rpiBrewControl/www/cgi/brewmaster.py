#!/usr/bin/env python

import cgitb; cgitb.enable()
import cgi
import os
import sys

os.chdir("../../")
sys.path.append(os.getcwd())

print "Content-Type: text/html\n"
print os.getcwd()

from dbFunctions import *
from configFunctions import *

global config
config = yaml.load(file("config.yml"))

# Load Configuration into Sensor Classes
sensors = loadSensorConfig(config)

# Create database connection
conn = sqlite3.connect("../../"+config['dbFile'])

input_data  = cgi.FieldStorage()
if input_data['func'].value == "equipSummary":
	print "equipment summary"
	for sensor in sensors:
		print sensor.id +": " + sensor.name
else:
	print "hello"
