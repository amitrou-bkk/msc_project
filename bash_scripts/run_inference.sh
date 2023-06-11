#!/bin/bash 
source ../../venv373/bin/activate
PYTHONPATH="/home/amitrou/msc_project" YOLO_MODEL="/home/amitrou/yolov5" IMG_PREDICTION_REPO="/app/edge_shared_files/image_inference" ML_MODEL_WEIGHTS_DIR="/app/edge_shared_files/ml_weights" python3 /home/amitrou/msc_project/src/app.py inference_controller