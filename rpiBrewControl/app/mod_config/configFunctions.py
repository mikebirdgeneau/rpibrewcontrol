
# Class for sensorSettings
class sensorSettings:
    def __init__(self, id = "28-xxxxxxxxxxxx", name = "Vessel", heatPin = 99,
    heaterEnabled = 0, set_point = 0.0, alarmLL = -0.1, alarmHH = 100.0, 
    alarmTolL = 5.0, alarmTolH = 5.0, Kc = 44, Ti = 165, Td = 4.0, Ts = 5.0, 
    smoothPts = 5):
        self.id = id
        self.name = name
        self.heatPin = heatPin
        self.heaterEnabled = heaterEnabled
        self.temp_C = -99
        self.set_point = set_point
        self.duty_cycle = 0.0
        self.alarmLL = alarmLL
        self.alarmHH = alarmHH
        self.alarmTolL = alarmTolL
        self.amarlTolH = alarmTolH
        self.Kc = Kc
        self.Ti = Ti
        self.Td = Td
        self.cycle_time = Ts
        self.smoothPts = smoothPts
        self.elapsed = 0.5
        
# Load Configuration into Sensor Classes
def loadSensorConfig(config):
    sensors = [ ]
    for sensor in config['sensors']:
        #print sensor
        thisSensor = sensorSettings(id=sensor['id'],name=sensor['name'], 
            heatPin = sensor['heatPin'], heaterEnabled = sensor['heaterEnabled'],
            set_point = sensor['defaultSetpoint'],alarmLL = sensor['alarmLL'], 
            alarmHH = sensor['alarmHH'],Kc = sensor['Kc'],Ti = sensor['Ti'],
            Td = sensor['Td'], Ts = sensor['Ts'], 
            smoothPts = sensor['smoothPts'])
        sensors.append(thisSensor)
    return(sensors)
    
def updateSensorConfig(config,sensors):
    # TODO: Load configuration files, and update settings that have changed.
    # Should not update the setpoint though... since this will come from the DB.
    return(sensors)