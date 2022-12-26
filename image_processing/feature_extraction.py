from src.image_processing.SIFT import SIFT
import numpy as np 
from src.db.mongoDbClient import MongoDbClient
import uuid
import os
import bson
import time
import src.utilities.file as fileUtils

class FeatureExtractor:
    def __init__(self, train_files, storage_provider):
        self.training_data = train_files
        self.storage_provider = storage_provider
        self.loggerFilePath =  os.path.join("/app/edge_shared_files", "logs", "feature_extractor.log")

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
            
        processor = SIFT()
        print(f"Is Continuius:{isContinuousLoop}-{self.training_data}-{self.loggerFilePath}")

        if not os.path.exists(os.path.join("/app/edge_shared_files", "logs")):
            os.makedirs(os.path.join("/app/edge_shared_files", "logs"))

        while True: 
            if not self.storage_provider.path_exists(self.training_data):
                fileUtils.write_text_to_file(f"{self.training_data} doesnot exist",self.loggerFilePath)
                continue
            
            print("Started Extracting Features")
            fileUtils.write_text_to_file( "Started Extracting Features", self.loggerFilePath)

            files =  self.storage_provider.read_directory(self.training_data)

            for file in files:
                print(f"SHIFT processing for file {file}")

                fileUtils.write_text_to_file(f"SHIFT processing for file {file}", self.loggerFilePath)
                
                if self.FeaturesExistForFile(file):
                    print(f"SHIFT features for file {file} exist")
                    continue

                try:
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
                    else:
                        shiftFilename , _ = fileUtils.get_filename_and_extension(file)
                        fileUtils.write_text_to_file( f"Saving descriptor in os.path.join(self.training_data, {shiftFilename}.descriptor", self.loggerFilePath)
                        fileUtils.save_array_to_file(descriptors, os.path.join(self.training_data, f"{shiftFilename}"))
                except Exception as ex:
                    pass
           
            time.sleep(10)

            if not isContinuousLoop:
                break


    def FeaturesExistForFile(self, file):
        shiftFilename , _ = fileUtils.get_filename_and_extension(file)
        return self.storage_provider.path_exists( os.path.join(self.training_data,f"{shiftFilename}.npy"))

    
       



