#!/bin/bash

chmod +x $PWD"/VSC/Systecs-Gebaeudeanalyse/RPI/Deployment/Scripts/startupPOST.sh" &

mkdir ~/.config/autostart
touch ~/.config/autostart/autostart.desktop
echo "[Desktop Entry]" > ~/.config/autostart/autostart.desktop
echo "Name=Autostart" >> ~/.config/autostart/autostart.desktop
echo "Exec="$PWD"/VSC/Systecs-Gebaeudeanalyse/RPI/Deployment/Scripts/startupPOST.sh" >> ~/.config/autostart/autostart.desktop
echo "Type=Application" >> ~/.config/autostart/autostart.desktop