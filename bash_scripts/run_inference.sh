#!/bin/bash 
source ../../venv373/bin/activate
PYTHONPATH="/home/amitrou/msc_project" YOLO_MODEL="/home/amitrou/yolov5" IMG_PREDICTION_REPO="/app/edge_shared_files/image_inference" ML_MODEL_WEIGHTS_DIR="/app/edge_shared_files/ml_weights" ML_MODEL_RESULTS_DIR="/app/edge_shared_files/inference_results" python3 /home/amitrou/msc_project/src/inference_controller_app.py