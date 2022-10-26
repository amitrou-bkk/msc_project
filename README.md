# Welcome to my project !

This project is an edge computing platform called **MEC**. 

## Docker
Run the following commands
In project directory run

### Feature Extractor Docker
docker build -t extractor -f ./docker/feature-extraction.dockerfile .<br>
docker run extractor<br>


## Docker Compose
docker-compose -f ./docker/cloud-docker-compose.yml up

