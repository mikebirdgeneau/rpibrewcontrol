#!/bin/sh

## Install python yaml module:
sudo apt-get install python-yaml

## Install RPi.GPIO
wget http://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.1.0.tar.gz
tar zxf RPi.GPIO-0.1.0.tar.gz
cd RPi.GPIO-0.1.0
sudo python setup.py install
cd ..

sudo pip install subprocess
#sudo pip install matplotlib
sudo pip install pushbullet.py
sudo pip install simplejson
#sudo pip install python-nvd3

## Install Apache to server frontend
sudo apt-get install apache2
sudo pip install flask

### NOT USING STUFF BELOW HERE AT THE MOMENT:
## Install flask-appbuilder & dependencies (http://flask-appbuilder.readthedocs.org/en/latest/installation.html)
sudo pip install flask-appbuilder
sudo pip install virtualenv
cd rpiBrewControl
fabmanager create-app
# type "frontend" as name of app.
cd frontend
fabmanager create-admin # Add your info for the admin user...
