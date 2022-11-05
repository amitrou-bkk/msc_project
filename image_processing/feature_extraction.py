from src.image_processing.SIFT import SIFT
from src.db.mongoDbClient import MongoDbClient
import os
class FeatureExtractor:
    def __init__(self, train_files="andreas"):
        self.training_data = train_files

    def ExtractFeatures(self):
        processor = SIFT()
        if os.getenv("DB_HOST") != None and os.getenv("DB_HOST") != "":
            print("Found database usage. Attempting to connect")
            self.client = MongoDbClient(os.getenv("DB_HOST"), "", os.getenv("DB_PORT"), os.getenv("DB_USER"),os.getenv("DB_PASSWORD"))
            self.client.connect()
        if not os.path.exists(self.training_data):
            print("Dir was not found")
            return

        print("Started Extracting Features")
        for file in self.training_data:
            _, descriptors = processor.GenerateKeyPointsAndDescriptors(file)
            print(descriptors)
            


