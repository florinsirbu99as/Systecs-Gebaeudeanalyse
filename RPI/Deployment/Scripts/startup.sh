#!/bin/bash

cd ~
source env/bin/activate
python ~/VSC/Systecs-Gebaeudeanalyse/RPI/AMG8833_IR_cam-main/detailed.py &
deactivate

obs --startstreaming