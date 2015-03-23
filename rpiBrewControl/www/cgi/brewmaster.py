#!/usr/bin/env python

import cgitb; cgitb.enable()
import cgi
import os
import sys

os.chdir("../../")
sys.path.append(os.getcwd())

print "Content-Type: text/html\n"
#print os.getcwd()

from dbFunctions import *
from configFunctions import *

input_data  = cgi.FieldStorage()
if input_data['func'].value == "equipSummary":
	print "Equipment Summary"
else:
	print "hello"
