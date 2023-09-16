import json
import uuid
import os
from src.services.event_triggered_service import EventTriggeredService, NotificationData
from src.storage.AzureBlobStorage import AzureBlobStorage
import src.utilities.file as fileUtils

class CloudUploadBlobService(EventTriggeredService):
    def __init__(self, storage_account, sas_token) -> None:
        self.blob_service = AzureBlobStorage(storage_account, sas_token)

    def UploadInferenceResultsAsBlob(self, results, container_name):
        local_file_name = str(uuid.uuid4()) + ".json"
        if results != None and len(results) == 0:
            return 
        with open(local_file_name, "w") as file:
            json.dump(results, file)
        
        self.blob_service.write_file(local_file_name, container_name)
                
    def TransformResults(self, results : list) -> list:
        upload_data = []
        if results == None:
            return upload_data
        
        for item in results:
            ul, lr, confidence, label = item
            values = dict()
            values["UX"] = list(ul)
            values["RY"] = list(lr)
            values["confidence"] = round(confidence, 3)
            values["label"] = label
            upload_data.append(values)

        return upload_data
    
    def OnNotified(self, notification: NotificationData) -> bool:
        data = json.loads(notification.data)
        local_file = data["file"]
        target_container = data["container"]

        if not fileUtils.fileOrDirectoryExists(local_file):
            return False
        
        try:
            file_data = fileUtils.read_json(file_path= local_file)
            transformed_data = self.TransformResults(file_data)
            print(transformed_data)
            self.UploadInferenceResultsAsBlob(transformed_data, container_name= target_container)
            return True
        except Exception as ex:
            print(ex)
            return False


        