# Welcome MSc project thesis.

 
## Run using docker
Docker and Docker Compose needs to be installed.
 1. Go to **src/docke**r directory and edit the following files:
 - **edge-camera-controller-phone-cam-01.dockerfile** 
       Edit the ENV variables   
       ENV CAMERA_IP="<IP of ESP 32 camera>" 
       ENV CAMERA_PORT="<PORT of ESP 32 camera>"  
       ENV CAMERA_USERNAME="<username for login ESP 32 camera>"  
       ENV CAMERA_PASSWORD="<password for login ESP 32 camera>"
    2. **edge-ingress-controller.dockerfile**  No need to edit or add any ENV variable
    3. **edge-inference-controller.dockerfile**  No need to edit or add any ENV variable
    4. ****edge-messaging-controller.dockerfile*** 
	   In case you want to use a specific storage account edit the AZURE_STORAGE_ACCOUNT variable  otherwise contact the owner of the repository to provide you with the default one.
	   ENV AZURE_STORAGE_ACCOUNT="<storage_account>" 
	  In case you want to use a SAS_TOKEN for the blob storage in Azure edit the following ENV variable otherwise contact the owner of the repository	   	
       ENV AZURE_STORAGE_SAS_TOKEN="<sas_token>"   
      In case you want to use a different queue in Azure edit the following ENV variable otherwise contact the owner of the repository	   	
       ENV AZ_QUEUE_NAME="Azure Queue Name"
        In case you want to use a different queue in Azure and thus a different connection string edit the following ENV variable otherwise contact the owner of the repository
        ENV AZ_QUEUE_CONSTR="<Azure Queue Connection String>"
        	   	
2. Go to src directory and execute the following command.
docker-compose -f ./docker/edge-docker-compose.yml up

  
  

##  Run without using docker
The implementation was tested in **Ubuntu 20.04.5 LTS**
1, Install Python 3.7.3
2. Install Python virtual environment
3. Run python3 -m venv venv373
4. Go to directory src/bash and change the line 
source  ../../venv373/bin/activate
with the relative path the vevn373 is created.
5. Edit the variables the same way is described in the **Run Using Docker** section 
6. Change directory to /bash and execute the following commands in separate terminal sessions.
sudo ./run_camera.sh
sudo ./run_inference.sh
sudo ./run_ingest.sh
sudo ./run_message_controller.sh