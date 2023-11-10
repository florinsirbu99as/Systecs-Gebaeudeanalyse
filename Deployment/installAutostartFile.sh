#!/bin/bash

touch ~/.config/autostart/autostart.desktop
echo "[Desktop Entry]" > ~/.config/autostart/autostart.desktop
echo "Name=Autostart" >> ~/.config/autostart/autostart.desktop
echo "Exec="$PWD"/Scripts/startup.sh" >> ~/.config/autostart/autostart.desktop
echo "Type=Application" >> ~/.config/autostart/autostart.desktop