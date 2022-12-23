from src.image_processing.SIFT import SIFT
import numpy as np 
from src.db.mongoDbClient import MongoDbClient
import uuid
import os
import bson

class FeatureExtractor:
    def __init__(self, train_files, storage_provider):
        self.training_data = train_files
        self.storage_provider = storage_provider

    def PrepareFeatureDb(self, dbName):
        self.client.createDb(dbName)

    def __ShouldUseDb(self):
        return os.getenv("DB_HOST") != None and os.getenv("DB_HOST") != ""

    def __CanConnectToDb(self):       
            self.client = MongoDbClient(os.getenv("DB_HOST"), "", os.getenv("DB_PORT"), os.getenv("DB_USER"),os.getenv("DB_PASSWORD"))
            return self.client.connect()

    def ExtractFeatures(self, isContinuousLoop = False):
        if(self.__ShouldUseDb() and self.__CanConnectToDb()):
            self.PrepareFeatureDb("features_db")

        if not self.storage_provider.path_exists(self.training_data):
            print(f"Dir {self.training_data} was not found")
            return
            
        print("Started Extracting Features")

        processor = SIFT()

        while True: 
            files =  self.storage_provider.read_directory(self.training_data)
            for file in files:
                print(f"SHIFT processing for file {file}")
                _, descriptors = processor.GenerateKeyPointsAndDescriptors(self.storage_provider.read_file(file))
                print(f"""Descriptors Calculated: 
                            File: {file}
                            Descriptors: {descriptors}""")
                
                if self.__ShouldUseDb():
                    print("Saving to db")                
                    document = {
                        "id" : bson.objectid.ObjectId(),
                        "file_name" : file,
                        "descriptors": np.concatenate((descriptors,np.zeros((1,128))),axis=0).tolist()
                    }

                    self.client.add_document(document)
                    
            if not isContinuousLoop:
                break


    
       



