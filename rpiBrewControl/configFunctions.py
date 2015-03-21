
# Class for sensorSettings
class sensorSettings:
    def __init__(self, id = "28-xxxxxxxxxxxx", name = "Vessel", heatPin = 99,
    heaterEnabled = 0, set_point = 0.0, alarmLL = -0.1, alarmHH = 100.0, 
    alarmTolL = 5.0, alarmTolH = 5.0, Kc = 44, Ti = 165, Td = 4.0, Ts = 5.0, 
    num_pnts_smooth = 5):
        self.id = id
        self.name = name
        self.heatPin = heatPin
        self.heaterEnabled = heaterEnabled
        self.set_point = set_point
        self.alarmLL = alarmLL
        self.alarmHH = alarmHH
        self.alarmTolL = alarmTolL
        self.amarlTolH = alarmTolH
        self.Kc = Kc
        self.Ti = Ti
        self.Td = Td
        self.Ts = Ts
        self.num_pnts_smooth = num_pnts_smooth
    def __getitem__(self, i):
...     return self[i]
        
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
            num_pnts_smooth = sensor['smoothPts'])
        sensors.append(thisSensor)
    return(sensors)
    
def updateSensorConfig(config,sensors):
    return(sensors)