FROM python:3.8.10
WORKDIR /app
COPY requirements_messaging_controller.txt requirements_messaging_controller.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements_messaging_controller.txt
COPY ./ ./src
ENV PYTHONPATH="/app"
ENV STORAGE_PROVIDER="fs"
ENV INCOMING_IMG_REPO="/app/edge_shared_files/process_data" 
ENV AZURE_STORAGE_ACCOUNT="https://mlcloudstorageacount.blob.core.windows.net/"
ENV AZURE_STORAGE_SAS_TOKEN="<SAS_TOKEN>"
ENV AZ_QUEUE_NAME="yolotrainingresults"
ENV ML_MODEL_WEIGHTS_DIR="/app/edge_shared_files/ml_weights"
ENV ML_MODEL_RESULTS_DIR="/app/edge_shared_files/inference_results" 
ENV ML_MODEL_RESULTS_CONTAINER="inferenceresults" 
ENV AZ_QUEUE_CONSTR="<AZURE_QUEUE_CONNECTION_STRING"
ENV AZURE_INF_RESULTS_STORAGE_SAS_TOKEN="<SAS_TOKEN>"
ENV RUN_MODE="CONTINUOUS"
CMD ["python3", "./src/messaging_controller_app.py"]
