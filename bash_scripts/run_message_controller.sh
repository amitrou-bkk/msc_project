#!/bin/bash 
source ../../venv373/bin/activate
PYTHONPATH="/home/amitrou/msc_project" INCOMING_IMG_REPO="/app/edge_shared_files/process_data" AZ_QUEUE_CONSTR="DefaultEndpointsProtocol=https;AccountName=mlcloudstorageacount;AccountKey=YqZgl8Aiqbj7eeEpwXzs6Vt7m2qk4G9qPjSO800BDo+3z+bXa+91qw32GqMPXqMxxK2rVln7/Npo+AStE/QrzQ==;EndpointSuffix=core.windows.net" AZURE_STORAGE_ACCOUNT=""https://mlcloudstorageacount.blob.core.windows.net/"" AZURE_STORAGE_SAS_TOKEN="<TOKEN>"  AZ_QUEUE_NAME="yolotrainingresults" ML_MODEL_WEIGHTS_DIR="/app/edge_shared_files/ml_weights" ML_MODEL_RESULTS_DIR="/app/edge_shared_files/inference_results" ML_MODEL_RESULTS_CONTAINER="inferenceresults" AZURE_INF_RESULTS_STORAGE_SAS_TOKEN="<TOKEN>" python3 /home/amitrou/msc_project/src/messaging_controller_app.py