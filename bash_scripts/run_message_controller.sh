#!/bin/bash 
source ../../venv373/bin/activate
PYTHONPATH="/home/amitrou/msc_project" AZURE_STORAGE_ACCOUNT="<storage_account>" AZURE_STORAGE_SAS_TOKEN="<sas_token>" AZ_QUEUE_NAME="yolotrainingresults" ML_MODEL_WEIGHTS_DIR="/app/edge_shared_files" python3 /home/amitrou/msc_project/src/app.py messaging_controller