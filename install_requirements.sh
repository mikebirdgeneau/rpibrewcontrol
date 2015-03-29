#!/bin/sh

# Update aptitude & upgrade to latest versions:
sudo apt-get update
sudo apt-get upgrade

# Install the stack
apt-get install build-essential python-dev # python development files
sudo apt-get install python-pip # python package manager
sudo apt-get install nginx  # web server
sudo apt-get install mariadb-server # mysql server
sudo apt-get install python-yaml

# Install python modules
sudo easy_install -U distribute
sudo pip install uwsgi

#sudo pip install tornado
sudo pip install RPi.GPIO
sudo pip install subprocess
sudo pip install pushbullet.py
sudo pip install simplejson
sudo pip install python-mysqldb
sudo pip install awscli
# AWS CLI used to roll my own Dynamic DNS service
# Not required!
# http://willwarren.com/2014/07/03/roll-dynamic-dns-service-using-amazon-route53/


## Install RPi.GPIO # try using pip to install above, or use manual install as follows
#wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.1.0.tar.gz
#tar zxf RPi.GPIO-0.1.0.tar.gz
#cd RPi.GPIO-0.1.0
#sudo python setup.py install
#cd ..

# Get MongoDB (instead of SQLite) for Async requests
# https://github.com/svvitale/mongo4pi (can also compile from scratch, but it's slow!)
git clone https://github.com/svvitale/mongo4pi.git
cd mongo4pi
./install.sh
cd ..

#curl -OL https://mms.mongodb.com/download/agent/automation/mongodb-mms-automation-agent-1.7.1.1023-1.linux_x86_64.tar.gz
#tar -xvf mongodb-mms-automation-agent-1.7.1.1023-1.linux_x86_64.tar.gz
#cd mongodb-mms-automation-agent-1.7.1.1023-1.linux_x86_64
#vi local.config
## MANUALLY ADD KEYS
sudo mkdir /var/lib/mongodb-mms-automation
sudo mkdir /var/log/mongodb-mms-automation
sudo mkdir -p /data
sudo chown `whoami` /var/lib/mongodb-mms-automation
sudo chown `whoami` /var/log/mongodb-mms-automation
sudo chown `whoami` /data
nohup ./mongodb-mms-automation-agent --config=local.config >> /var/log/mongodb-mms-automation/automation-agent.log 2>&1 &

## Install NGINX to server frontend
#sudo apt-get install nginx

### NOT USING STUFF BELOW HERE AT THE MOMENT:
## Install flask-appbuilder & dependencies (http://flask-appbuilder.readthedocs.org/en/latest/installation.html)
#sudo pip install flask-appbuilder
#sudo pip install virtualenv
#cd rpiBrewControl
#fabmanager create-app
# type "frontend" as name of app.
#cd frontend
#fabmanager create-admin # Add your info for the admin user...
