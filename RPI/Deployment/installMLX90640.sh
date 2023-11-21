#!/bin/bash

#write Baudrate settings
sudo python ~/VSC/Systecs-Gebaeudeanalyse/RPI/Deployment/Scripts/writeBaudrate.py

#install matplotlib
sudo apt update
sudo apt upgrade
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
pip3 install pithermalcam --verbose
deactivate
#source env/bin/activate