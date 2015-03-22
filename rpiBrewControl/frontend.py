# Nothing here yet!! :)

from flask import Flask
import numpy as np
import cStringIO
import matplotlib.pyplot as plt
import sqlite3
from dbFunctions import *


app = Flask(__name__)

@app.route('/plot')
def build_plot():

  # Generate the plot
  x = np.linspace(0, 10)
  line, = plt.plot(x, np.sin(x))

  f = cStringIO.StringIO()
  plt.savefig(f, format='png')

  # Serve up the data
  header = {'Content-type': 'image/png'}
  f.seek(0)
  data = f.read()

  return data, 200, header

if __name__ == '__main__':
  app.run()

# Planned Functionality:
#- Summary Table of Sensors / Status
#- View Trends vs. Setpoints
#- Change Setpoints
#- Change PID settings
#- Export Data / Charts 