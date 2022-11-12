FROM python:3.8.10
WORKDIR /app
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 git  -y
RUN mkdir src
RUN git clone https://github.com/amitrou-bkk/msc_project.git src
RUN pip install -r ./src/requirements.txt
ENV PYTHONPATH="/app"
ENV DB_HOST="mongo"
ENV DB_PORT="27017"
ENV DB_USER="root"
ENV DB_PASSWORD="example"
ENV FILE_DIR="local:"
CMD ["python3", "./src/app.py", "feature_extractor"]
