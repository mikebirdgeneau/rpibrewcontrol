import datetime

def add_temp_reading(conn,curTime,id,temp):
    curs = conn.cursor()
    if temp!=-99:
        curs.execute("CREATE TABLE IF NOT EXISTS temperatures (time datetime, id text, tempC real)")
        curs.execute("INSERT INTO temperatures values(datetime(?),(?), (?))", (curTime,id,temp))
        conn.commit()
        return 0
    else:
        print id + ": Invalid reading, check if sensor is connected."
        return 1
        
def get_temp_data_for_sensor(conn,id,limitTime = datetime.datetime.utcnow()-datetime.timedelta(hours=12)):
    curs = conn.cursor()
    curs.execute("SELECT * FROM temperatures WHERE id = '"+id+"' AND time > datetime('"+limitTime.strftime('%Y-%m-%d %H:%M:%S')+"')")
    rows = curs.fetchall()
    return rows
    

def add_temp_setpoint(conn,id,setTime,setTempC):
    curs = conn.cursor()
    # Needs improved error checking (e.g. within alarm ranges)
    if setTempC!=-99:
        curs.execute("CREATE TABLE IF NOT EXISTS setpoints (time datetime, id text, temp real)")
        curs.execute("INSERT INTO setpoints values(datetime(?),(?), (?))", (setTime,id,setTempC))
        conn.commit()
        return 0
    else:
        print id + ": Invalid reading, check if sensor is connected."
        return 1
        
def remove_temp_setpoint(conn,id,setTime):
    curs = conn.cursor()
    curs.execute("DELETE FROM setpoints WHERE id = '"+id+"' AND time = datetime('"+limitTime.strftime('%Y-%m-%d %H:%M:%S')+"')")
    curs.commit()
    return 0
    
def get_setpoint_for_sensor(conn,id):
    curs = conn.cursor()
    curs.execute("SELECT * FROM setpoints WHERE id = '"+id+"'")
    rows = curs.fetchall()
    return rows
    
    
def add_duty_reading(conn,curTime,id,duty_cycle,set_point):
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS duty (time datetime, id text, duty real, setpoint real)")
    curs.execute("INSERT INTO duty values(datetime(?),(?),(?),(?))", (curTime,id,duty_cycle,set_point))
    conn.commit()
    return 0
