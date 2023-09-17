FROM python:3.8.10
WORKDIR /app
COPY requirements_ingestion_controller.txt requirements_ingestion_controller.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements_ingestion_controller.txt
COPY ./ ./src
ENV PYTHONPATH="/app"
CMD ["python3", "./src/ingestion_controller_app.py"]
