FROM python:3.8.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 git  -y
RUN git clone https://github.com/ultralytics/yolov5.git
RUN pip install -r  requirements.txt
COPY ./ ./src
ENV PYTHONPATH="/app"
ENV STORAGE_PROVIDER="fs"
ENV IMG_PREDICTION_REPO="/app/edge_shared_files/image_inference"
ENV YOLO_MODEL="/app/yolov5"
ENV ML_MODEL_WEIGHTS_DIR="/app/edge_shared_files/ml_weights"
ENV ML_MODEL_RESULTS_DIR="/app/edge_shared_files/inference_results"
ENV RUN_MODE="CONTINUOUS"
RUN ls .
CMD ["python3", "./src/app.py", "inference_controller"]
