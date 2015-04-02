
# Class for sensorSettings
class sensorSettings:
    def __init__(self, id = "28-xxxxxxxxxxxx", name = "Vessel", heatPin = 99,
    heaterMode = 0, sensorEnabled = 0, set_point = 0.0, alarmLL = -0.1, 
    alarmHH = 100.0, alarmL = -0.1, alarmH = 100.0, Kc = 44, Ti = 165, Td = 4.0, 
    Ts = 5.0, smoothPts = 5, record_freq = 10.0):
        self.id = id
        self.name = name
        self.heatPin = heatPin
        self.heaterMode = heaterMode
        self.sensorEnabled = sensorEnabled
        self.temp_C = -99
        self.set_point = set_point
        self.duty_cycle = 0.0
        self.alarmLL = alarmLL
        self.alarmHH = alarmHH
        self.alarmL = alarmL
        self.alarmH = alarmH
        self.Kc = Kc
        self.Ti = Ti
        self.Td = Td
        self.cycle_time = Ts
        self.record_freq = record_freq
        self.smoothPts = smoothPts
        self.elapsed = 0.5
        
# Load Configuration into Sensor Classes
def loadSensorConfig(config):
    sensors = [ ]
    for sensor in config['sensors']:
        #print sensor
        thisSensor = sensorSettings(id=sensor['id'],name=sensor['name'], 
            heatPin = sensor['heatPin'], heaterMode = sensor['heaterMode'],
            sensorEnabled = sensor['sensorEnabled'],
            set_point = sensor['defaultSetpoint'],alarmLL = sensor['alarmLL'], 
            alarmHH = sensor['alarmHH'],Kc = sensor['Kc'],Ti = sensor['Ti'],
            Td = sensor['Td'], Ts = sensor['Ts'], record_freq = sensor['record_freq'],
            smoothPts = sensor['smoothPts'])
        sensors.append(thisSensor)
    return(sensors)
    