#!/bin/sh

# Update aptitude & upgrade to latest versions:
sudo apt-get update
sudo apt-get upgrade

# Install pip & easy install
sudo apt-get install python-pip
sudo easy_install -U distribute

## Install python yaml module:
sudo apt-get install python-yaml

# Install python modules:
sudo pip install tornado
sudo pip install RPi.GPIO
sudo pip install subprocess
sudo pip install pushbullet.py
sudo pip install simplejson

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
