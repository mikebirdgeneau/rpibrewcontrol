
class Sensor(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sensor_id = db.Column(db.String(16), unique=True)
    name = db.Column(db.String(80))
    heatPin = db.Column(db.Integer,unique=True)
    heaterMode = db.Column(db.Integer)
    sensorEnabled = db.Column(db.Integer)
    setPoint = db.Column(db.Numeric(2))
    dutyCycle = db.Column(db.Numeric(2))
    alarmLL = db.Column(db.Numeric(2))
    alarmHH = db.Column(db.Numeric(2))
    alarmL = db.Column(db.Numeric(2))
    alarmH = db.Column(db.Numeric(2)) 
    pidKc = db.Column(db.Numeric(2)) 
    pidTi = db.Column(db.Numeric(2))     
    pidTd = db.Column(db.Numeric(2))
    Ts = db.Column(db.Numeric(2))
    smoothPts = db.Column(db.Integer)
    updated = db.Column(db.DateTime(False))
    readings = db.relationship('Reading', backref='sensor', lazy='dynamic')
    setpoints = db.relationship('Setpoint', backref='sensor', lazy='dynamic')

    
    def __init__(self, name, heatPin, heaterMode, sensorEnabled, setPoint, 
        dutyCycle, alarmLL, alarmHH, alarmL, alarmH, pidKc, pidTi, pidTd, Ts, 
        smoothPts, updated):
        self.name = name
        self.heatPin = heatPin
        self.heaterMode = heaterMode
        self.sensorEnabled = sensorEnabled
        self.setPoint = setPoint 
        self.dutyCycle = dutyCycle
        self.alarmLL = alarmLL
        self.alarmHH = alarmHH 
        self.alarmL = alarmL
        self.alarmH = alarmH
        self.pidKc = pidKc
        self.pidTi = pidTi
        self.pidTd = pidTd
        self.Ts = Ts
        self.smoothPts = smoothPts
        self.updated = updated

    def __repr__(self):
        return '<Sensor %r>' % self.id
        
class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(16), db.ForeignKey('sensor.sensor_id'))
    time = db.Column(db.DateTime(False))
    tempC = db.Column(db.Numeric(2))
    setPoint = db.Column(db.Numeric(2))
    dutyCycle = db.Column(db.Numeric(2))
    heaterMode = db.Column(db.Integer)


    def __init__(self, sensor_id, tempC, setPoint, dutyCycle, heaterMode):
        self.sensor_id = sensor_id
        self.time = datetime.datetime.utcnow()
        self.tempC = tempC
        self.setPoint = setPoint
        self.dutyCycle = dutyCycle
        self.heaterMode = heaterMode

class Setpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(16), db.ForeignKey('sensor.sensor_id'))
    time = db.Column(db.DateTime(False))
    setPoint = db.Column(db.Numeric(2))

    def __init__(self, sensor_id, time, setPoint):
        self.sensor_id = sensor_id
        self.time = time
        self.setPoint = setPoint


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)
