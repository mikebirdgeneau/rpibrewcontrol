from subprocess import Popen, PIPE, call
from multiprocessing import Process, Pipe, Queue, current_process
from Queue import Full

import time, os, signal, sys
import RPi.GPIO as GPIO

global ON, OFF
ON = 1
OFF = 0


# Initialize GPIO Settings
def initializeGPIO(config):
    GPIO.setmode(GPIO.BCM)
    for sensor in config['sensors']:
        if sensor['heaterMode'] != 0:
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
    
# Standalone Process to get Temperatures
def gettempProc(proc, sensor):
    p = current_process()
    print 'Starting:', p.name, p.pid
    
    while (True):
        t = time.time()
        time.sleep(.5) #.1+~.83 = ~1.33 seconds
        num = tempData1Wire(sensor.id)
        elapsed = "%.2f" % (time.time() - t)
        proc.send([num, sensor.id, elapsed])

#Get time heating element is on and off during a set cycle time
def getonofftime(cycle_time, duty_cycle):
    duty = duty_cycle/100.0
    on_time = cycle_time*(duty)
    off_time = cycle_time*(1.0-duty)   
    return [on_time, off_time]

# Stand Alone Heat Process using GPIO
def heatProcGPIO(proc, sensor):
    p = current_process()
    #signal.signal(signal.SIGINT, original_sigint_handler)
    print 'Starting:', p.name, p.pid
    if sensor.heatPin > 0:
        GPIO.setup(sensor.heatPin, GPIO.OUT)
        while (True):
            while (proc.poll()): #get last
                sensor.cycle_time, sensor.duty_cycle = proc.recv()
            proc.send([sensor.cycle_time, sensor.duty_cycle])  
            if sensor.duty_cycle == 0:
                GPIO.output(sensor.heatPin, OFF)
                time.sleep(sensor.cycle_time)
            elif sensor.duty_cycle == 100:
                GPIO.output(sensor.heatPin, ON)
                time.sleep(sensor.cycle_time)
            else:
                on_time, off_time = getonofftime(sensor.cycle_time, sensor.duty_cycle)
                GPIO.output(sensor.heatPin, ON)
                time.sleep(on_time)
                GPIO.output(sensor.heatPin, OFF)
                time.sleep(off_time)
