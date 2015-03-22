# Nothing here yet!! :)

from flask import Flask
#import numpy as np
#import cStringIO
#import matplotlib.pyplot as plt
import sqlite3
from dbFunctions import *


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# Planned Functionality:
#- Summary Table of Sensors / Status
#- View Trends vs. Setpoints
#- Change Setpoints
#- Change PID settings
#- Export Data / Charts 