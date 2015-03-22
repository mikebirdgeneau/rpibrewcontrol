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
sudo pip install matplotlib
sudo pip install pushbullet.py

## Install Apache to server frontend
sudo apt-get install apache2

pip install flask-appbuilder
