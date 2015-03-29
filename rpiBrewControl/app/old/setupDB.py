import MySQLdb 

password = raw_input("Please enter root password for MySQL: ")

def connect_to_database(user, password):
    return MySQLdb.connect(host='localhost', user=user, passwd=password) 


def create_database(cursor):
    cursor.execute('CREATE DATABASE brewPi')
    cursor.execute('USE brewPi')
    cursor.execute("CREATE USER 'brewPi'@'localhost' IDENTIFIED BY 'brewPi'");
    cursor.execute("GRANT ALL PRIVILEGES ON brewPi . * TO 'brewPi'@'localhost';")
    return 0
    
con = connect_to_database("root",password)
curs = con.cursor()
create_database(curs)
