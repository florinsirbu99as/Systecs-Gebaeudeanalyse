# Systecs-Gebaeudeanalyse

Setup Branch for the IR Camera AMG8833 on a Raspberry Pi 4

you need to install certain python packages and also OBS via Pi Apps

## Setup

Run **installMLX90640.sh** in RPI/Deployment to install necessary Python Libraries 
and Pi Apps, which is necessary for OBS installation

## Autostart

Run **installAutostartPOST.sh** in RPI/Deployment for the Autostart setting for an external Server.
Run **installAutostartFlaskAndMLX.sh** in RPI/Deployment for the Autostart setting for an external Server.
Run **uninstallAutostart.sh** in RPI/Deployment to remove Autostart setting.

## Config

### External Server

In the File **POSTServer\POSTScript.py** in line 22 you will have to set URL for the endpoint for the POST Request.

