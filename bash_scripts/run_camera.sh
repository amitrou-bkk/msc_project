#!/bin/bash 
source ../../venv373/bin/activate
PYTHONPATH="/home/amitrou/msc_project" QT_X11_NO_MITSHM=1 CAMERA_IP="192.168.1.12" CAMERA_PORT="81" CAMERA_ID="esp32" CAMERA_EXTRA_PATH="stream" python3 /home/amitrou/msc_project/src/app.py camera_controller