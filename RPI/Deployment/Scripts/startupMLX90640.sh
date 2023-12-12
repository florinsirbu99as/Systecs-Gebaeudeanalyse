#!/bin/bash

cd ~
source env/bin/activate
python ~/VSC/Systecs-Gebaeudeanalyse/Flask/Web/Camera.py &
python ~/VSC/Systecs-Gebaeudeanalyse/Flask/Web/app.py 
deactivate

