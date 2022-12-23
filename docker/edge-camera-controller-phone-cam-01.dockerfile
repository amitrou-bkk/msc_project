FROM python:3.8.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
COPY ./ ./src
ENV PYTHONPATH="/app"
ENV CAMERA_ID="PHONE_CAM_01"
ENV CAMERA_IP=""
ENV CAMERA_PORT=""
ENV CAMERA_USERNAME=""
ENV CAMERA_PASSWORD=""
ENV STORAGE_PROVIDER="fs"
# ENABLE_CAMERA_STREAM_SIMULATION is used for simulating the streaming of camera captures when no camera is available
ENV ENABLE_CAMERA_STREAM_SIMULATION = "True"
CMD ["python3", "./src/app.py", "camera_controller"]
