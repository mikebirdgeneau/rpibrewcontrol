from subprocess import Popen, PIPE
import os
import signal
import sys
import RPi.GPIO as GPIO

def signal_handler(signal, frame):
        print "\n---\nCleaning up GPIO..."
        GPIO.cleanup()
        print "Terminating rpiBrewControl."
        sys.exit(0)

# Initialize GPIO Settings
def initializeGPIO(config):
    GPIO.setmode(GPIO.BCM)
    for sensor in config['sensors']:
        if sensor['heaterEnabled'] == 1:
           GPIO.setup(sensor['heatPin'],GPIO.OUT)

# Retrieve temperature from DS18B20 temperature sensor
def tempData1Wire(tempSensorId):
    if os.path.isfile("/sys/bus/w1/devices/w1_bus_master1/" + tempSensorId + "/w1_slave"):
        pipe = Popen(["cat","/sys/bus/w1/devices/w1_bus_master1/" + tempSensorId + "/w1_slave"], stdout=PIPE)
        result = pipe.communicate()[0]
        if (result.split('\n')[0].split(' ')[11] == "YES"):
            temp_C = float(result.split("=")[-1])/1000 # temp in Celcius
        else:
            temp_C = -99 #bad temp reading
    else:
            temp_C = -99 # Missing Device
    return temp_C