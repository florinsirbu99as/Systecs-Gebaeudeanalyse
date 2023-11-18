#!/bin/bash

#write Baudrate settings
sudo python ~/VSC/Systecs-Gebaeudeanalyse/RPI/Deployment/Scripts/writeBaudrate.py

#install matplotlib
sudo apt update
sudo apt install -y python3-matplotlib
sudo apt install -y python3-colour
sudo apt install -y python3-numpy
sudo apt install -y python3-scipy
sudo apt install -y python3.11-venv

#Setup a virtual python environment
cd ~
sudo python -m venv env --system-site-packages
source env/bin/activate

cd ~
pip3 install --upgrade adafruit-python-shell
pip3 install adafruit-circuitpython-amg88xx
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
deactivate
#source env/bin/activate

#Python Libraries
#pip3 install adafruit-circuitpython-amg88xx

#install Pi-Apps for OBS
wget -qO- https://raw.githubusercontent.com/Botspot/pi-apps/master/install | bash
