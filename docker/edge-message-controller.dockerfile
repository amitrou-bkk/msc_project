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
ENV AZURE_STORAGE_SAS_TOKEN="sp=rl&st=2023-06-10T11:58:48Z&se=2023-07-01T19:58:48Z&spr=https&sv=2022-11-02&sr=c&sig=W%2BAreurEqbgc353imUDHN0GAz9EaJSJSzx2g6TzfI1U%3D"
ENV AZ_QUEUE_NAME="yolotrainingresults"
ENV ML_MODEL_WEIGHTS_DIR="/app/edge_shared_files/ml_weights"
ENV ML_MODEL_RESULTS_DIR="/app/edge_shared_files/inference_results" 
ENV ML_MODEL_RESULTS_CONTAINER="inferenceresults" 
ENV AZ_QUEUE_CONSTR="DefaultEndpointsProtocol=https;AccountName=mlcloudstorageacount;AccountKey=YqZgl8Aiqbj7eeEpwXzs6Vt7m2qk4G9qPjSO800BDo+3z+bXa+91qw32GqMPXqMxxK2rVln7/Npo+AStE/QrzQ==;EndpointSuffix=core.windows.net"
ENV AZURE_INF_RESULTS_STORAGE_SAS_TOKEN="sp=rwl&st=2023-06-18T10:05:53Z&se=2023-07-20T18:05:53Z&spr=https&sv=2022-11-02&sr=c&sig=1on8pNwjlteY0qIoM8c2CUIB3axAA5JU2VaYWLKaF4o%3D"
ENV RUN_MODE="CONTINUOUS"
CMD ["python3", "./src/messaging_controller_app.py"]
