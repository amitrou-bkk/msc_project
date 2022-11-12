from src.image_processing.SIFT import SIFT
import numpy as np 
from src.db.mongoDbClient import MongoDbClient
import uuid
import os

class FeatureExtractor:
    def __init__(self, train_files="andreas"):
        self.training_data = train_files

    def PrepareFeatureDb(self, dbName):
        self.client.createDb(dbName)

    def __ShouldUseDb(self):
        return os.getenv("DB_HOST") != None and os.getenv("DB_HOST") != ""

    def __CanConnectToDb(self):       
            self.client = MongoDbClient(os.getenv("DB_HOST"), "", os.getenv("DB_PORT"), os.getenv("DB_USER"),os.getenv("DB_PASSWORD"))
            return self.client.connect()

    def ExtractFeatures(self):
        if(self.__ShouldUseDb() and self.__CanConnectToDb()):
            self.PrepareFeatureDb("features_db")

        if not os.path.exists(self.training_data):
            print("Dir was not found")
            return
            
        print("Started Extracting Features")

        processor = SIFT()
        for file in self.training_data:
            _, descriptors = processor.GenerateKeyPointsAndDescriptors(file)
            print(f"""Descriptors Calculated: 
                        File: {file}
                        Descriptors: {descriptors}""")
            
            if self.__ShouldUseDb():
                print("Saving to db")
                
                document = {
                    "id" : uuid.uuid4(),
                    "file_name" : file,
                    "descriptors": np.concatenate((descriptors,np.zeros((1,128))),axis=0) 
                  }

                self.client.add_document(document)


    
       



