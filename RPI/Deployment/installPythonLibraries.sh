#!/bin/bash

#write Baudrate settings
sudo python ~/VSC/Systecs-Gebaeudeanalyse/RPI/Deployment/Scripts/writeBaudrate.py

#install matplotlib
sudo apt install python3-matplotlib

#Setup a virtual python environment
cd ~
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py

source env/bin/activate

#Python Libraries
pip3 install adafruit-circuitpython-amg88xx
pip install colour

#install Pi-Apps for OBS
wget -qO- https://raw.githubusercontent.com/Botspot/pi-apps/master/install | bash
