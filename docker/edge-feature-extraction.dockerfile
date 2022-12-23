FROM python:3.8.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
COPY ./ ./src
ENV PYTHONPATH="/app"
ENV STORAGE_PROVIDER="fs"
ENV INPUT_DATA="/app/data_input"
ENV RUN_MODE="CONTINUOUS"
CMD ["python3", "./src/app.py", "feature_extractor"]
