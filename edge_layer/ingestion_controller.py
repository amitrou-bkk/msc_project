
import os
import shutil
import threading
import src.edge_layer.ingression_mode as IngressMode
from src.edge_layer.ingression_models.IngressionBase import DataIngressionConfiguration
from src.edge_layer.ingression_models.ingress_factory import IngressFactory
import src.utilities.file as fileUtils
from src.image_processing.keyframe_detector import KeyFrameDetector
from time import sleep

class IngestionController():
    
    def __init__(self):
        self.isStarted = False
        self.process_dir = "/app/edge_shared_files/process_data"
        self.allowedExtensions = [".jpg",".tiff", ".jpeg", ".img"]
        self.keyframe_extractor = KeyFrameDetector()

        self.threads = []

    def stage_file_for_process(self, img):
       print(f"Start Staging of {img}")
       if (not os.path.exists(self.process_dir)):
            os.mkdir(self.process_dir)

       file_name, file_extension = fileUtils.get_filename_and_extension(img)

       if (file_extension not in self.allowedExtensions):
            return
       
       staged_file = os.path.join(self.process_dir, os.path.basename(file_name) + file_extension)
       shutil.move(img, staged_file)
       print(f"Staged to Staging of {staged_file}")

    def startListening(self):
        self.isStarted = True
        print("Edge Controller Started.")
        for ingestionProvider in self.__getIngestionTypesFromConfiguration():
             print(type(ingestionProvider))
             sleep(5)
             ingestion_thread = threading.Thread(target= self.__readData, args = (ingestionProvider,))
             self.threads.append(ingestion_thread)
             ingestion_thread.start()


    def stopListening(self):
         print("Edge Controller Ending silently.")
         self.isStarted = False
         for thread in self.threads:
             thread.join()

    def __getIngestionTypesFromConfiguration(self):
        configurations = []
        factory = IngressFactory()
        data = fileUtils.read_json(os.path.join(os.path.dirname(__file__), "configuration.json"))
        available_cfgs = data["ingress_configurations"]
        for cfg in available_cfgs:
            if cfg["active"]:
                ingestionType = factory.create(cfg["mode"], cfg["parameters"])
                configurations.append(ingestionType)
        print("Configurations found:" + str(len(configurations)))
        sleep(5)
        return configurations
    
    def DetectIfImageIsKeyFrame(self, previous_image, current_image, algorithm="PBT"):
        isKeyframe = False

        if previous_image == None:
            isKeyframe = True
            return
        
        if algorithm == "PBT":
            isKeyframe = self.keyframe_extractor.PBT(previous_image, current_image, 0.8)
        elif algorithm == "HBT":
            isKeyframe = self.keyframe_extractor.HBT(previous_image, current_image)
        else:
            isKeyframe = True

        return isKeyframe


    def __readData(self, ingressProvider:DataIngressionConfiguration):
        keyframe_images = []
        non_keyframe_images = []

        while self.isStarted:
            try:
                print("Start Reading Data from Source")

                self.__removeNonKeyFrames(non_keyframe_images, 0) # tranfer leftovers
                self.__stageKeyframes(keyframe_images, 0) # tranfer leftovers

                last_image_path = None
                
                ingressProvider.read()
                image = ingressProvider.getNextData()
                
                while image != None :
                    print(f"Ingress: Reading file {image}")
                    image_path = os.path.join(ingressProvider.input_dir, image)
                    print(f"Entering Keyframe Detector")
                    isKeyFrame = self.DetectIfImageIsKeyFrame(last_image_path, image_path)
                    if isKeyFrame:
                        keyframe_images.append(image_path)
                    else:
                        non_keyframe_images.append(image_path)

                    if len(keyframe_images) + len(non_keyframe_images) == 5:
                       self.__removeNonKeyFrames(non_keyframe_images)
                       self.__stageKeyframes(keyframe_images)
                       
                    last_image_path = image_path
                    image = ingressProvider.getNextData()
                    print("Finished Reading Data.")
                sleep(2)
            except Exception as ex:
                print(ex)

    def __removeNonKeyFrames(self, non_keyframe_list, keep = 1):
         while len(non_keyframe_list) > keep:
            imageToRemove = non_keyframe_list.pop(0)
            os.remove(imageToRemove)

    def __stageKeyframes(self, keyframe_list, keep = 1):
        while len(keyframe_list) > keep:
             keyframe_to_stage = keyframe_list.pop(0)
             self.stage_file_for_process(keyframe_to_stage)





    




             