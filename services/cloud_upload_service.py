import json
import uuid
from src.storage.AzureBlobStorage import AzureBlobSorage

class CloudUploadBlobService:
    def __init__(self, storage_account, sas_token) -> None:
        self.blob_service = AzureBlobSorage(storage_account, sas_token)

    def UploadInferenceResultsAsBlob(self, results, container_name):
        local_file_name = str(uuid.uuid4()) + ".json"
        
        intermediate_data = self.TransformResults(results)
        
        with open(local_file_name, "w") as file:
            json.dump(intermediate_data, file)
        
        self.blob_service.write_file(results, container_name)
                
    def TransformResults(results : list) -> list:
        upload_data = []
        if results == None:
            return upload_data
        
        for item in results:
            ul, lr, confidence, label = item
            values = dict()
            values["UX"] = list(ul)
            values["RY"] - list(lr)
            values["confidence"] = confidence
            values["label"] = label
            upload_data.append(values)

        return upload_data



        