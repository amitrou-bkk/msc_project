from azure.storage.blob import BlobServiceClient
from src.storage.BaseStorage import BaseStorage
import os

class AzureBlobStorage(BaseStorage):
    def __init__(self, account, sas_token) -> None:
        self.seviceClient = BlobServiceClient(account_url=account, credential=sas_token)
        self.LOCAL_BLOB_PATH = "temp_azure"
        super().__init__()

    def create_directory(self, path):
       pass

    def read_directory(self, path):
       self.container_client = self.seviceClient.get_container_client(container= path) 
       blob_list = self.container_client.list_blobs()
       return [f"{path}:{blob.name}" for blob in blob_list]
   
    
    def write_file(self, input_file, container_name):
        self.container_client = self.seviceClient.get_container_client(container= container_name) 
        head, input_file = os.path.split(input_file)
        with open(file=input_file, mode="rb") as data:
            self.container_client.upload_blob(name=input_file, data=data)

    def path_exists(self, path):
         containers = self.seviceClient.list_containers()

         for container in containers:
            if container['name'] == path:
                return True

         return False

    def read_file(self, file):
        download_file_path = None
        container, blobfileName = str(file).split(":")

        self.container_client = self.seviceClient.get_container_client(container)
        blob_list = self.container_client.list_blobs()

        if not os.path.exists(self.LOCAL_BLOB_PATH):
             os.mkdir(self.LOCAL_BLOB_PATH)

        for blob in blob_list:
            if blob.name == blobfileName:
                 bytes = self.container_client.get_blob_client(blob).download_blob().readall()
                 download_file_path = os.path.join(self.LOCAL_BLOB_PATH, blobfileName)
                 with open(download_file_path, "wb") as file:
                    file.write(bytes)
                 break
                
        return download_file_path