#!/usr/bin/env python

import cgitb; cgitb.enable()
import cgi
import os

from ../../dbFunctions import *
from ../../configFunctions import *

input_data  = cgi.FieldStorage()
#if input_data:
print "Content-Type: text/html\n"
print "hello"
