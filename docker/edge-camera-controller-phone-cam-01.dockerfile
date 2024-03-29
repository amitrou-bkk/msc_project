FROM python:3.8.10
WORKDIR /app
COPY requirements_camera_controller.txt requirements_camera_controller.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements_camera_controller.txt
COPY ./ ./src
ENV PYTHONPATH="/app"
ENV CAMERA_ID="CAMERA_01"
ENV CAMERA_IP="192.168.1.12"
ENV CAMERA_EXTRA_PATH="stream"
ENV CAMERA_PORT="81"
ENV QT_X11_NO_MITSHM="1"
ENV CAMERA_USERNAME=""
ENV CAMERA_PASSWORD=""
ENV STORAGE_PROVIDER="fs"
# ENABLE_CAMERA_STREAM_SIMULATION is used for simulating the streaming of camera captures when no camera is available
ENV ENABLE_CAMERA_STREAM_SIMULATION="True"
CMD ["python3", "./src/camera_controller_app.py"]
