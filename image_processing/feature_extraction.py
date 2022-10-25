from src.image_processing.SIFT import SIFT
import os
class FeatureExtractor:
    def __init__(self, train_files="andreas"):
        self.training_data = train_files

    def ExtractFeatures(self):
        processor = SIFT()
        if not os.path.exists(self.training_data):
            print("Dir was not found")
            return

        print("Started Extracting Features")
        for file in self.training_data:
            _, descriptors = processor.GenerateKeyPointsAndDescriptors(file)
            print(descriptors)
            


