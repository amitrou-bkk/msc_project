from time import sleep
from src.machine_learning.YOLO.yolo import LocalYoloModel
import os

class InferenceController():
    def __init__(self, model_path, input_images_dir, weight_dir, output_results_dir = ModuleNotFoundError) -> None:
        weight = os.path.join(weight_dir, os.listdir(weight_dir)[0]) 
        self.model = LocalYoloModel(model_path, weight,  ['mask', 'no mask'])
        self.image_repo = input_images_dir

    def start(self):
        print("Inference started...")
        while True:
            for filename in os.listdir(self.image_repo):
                img = os.path.join(self.image_repo, filename)
                finame, file_extension = os.path.splitext(img)
                if str(file_extension).lower() == ".jpg":
                    print(f"Start prediction for {img}")
                    results = self.model.predict(img)
                    print("Results for: " + filename)
                    print(results)
                    os.remove(img)
            sleep(3)
            