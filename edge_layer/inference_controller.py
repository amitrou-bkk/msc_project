import os
from time import sleep
from src.machine_learning.YOLO.yolo import LocalYoloModel
import src.utilities.file as fileUtils

class InferenceController():
    def __init__(self, model_path, input_images_dir, weight_dir, output_results_dir = None) -> None:
        weight = os.path.join(weight_dir, os.listdir(weight_dir)[0]) 
        self.model = LocalYoloModel(model_path, weight,  ['mask', 'no mask'])
        self.image_repo = input_images_dir

        if output_results_dir != None:
            if not fileUtils.fileOrDirectoryExists(output_results_dir):
                fileUtils.createDirectory(output_results_dir)

        self.output_results_dir = output_results_dir
        print(f"Output inference dir: {self.output_results_dir}")

    def start(self):
        print("Inference started...")
        while True:
            for filename in os.listdir(self.image_repo):
                img = os.path.join(self.image_repo, filename)
                finame, file_extension = os.path.splitext(filename)
                if str(file_extension).lower() == ".jpg":
                    print(f"Start prediction for {img}")
                    results = self.model.predict(img)
                    if self.output_results_dir == None:
                        print("Results for: " + filename)
                        print(results)
                    else:
                        print(os.path.join(self.output_results_dir, finame + ".json"))
                        fileUtils.write_json(results, os.path.join(self.output_results_dir, finame + ".json"))
                    os.remove(img)
            sleep(3)
            