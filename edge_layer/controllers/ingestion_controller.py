import os
import shutil
import threading
from src.edge_layer.ingression_models.ingression_mode import EdgeDataIngressMode
from src.edge_layer.ingression_models.IngressionBase import IngressionBase
from src.edge_layer.ingression_models.ingress_factory import IngressFactory
import src.utilities.file as fileUtils
from src.image_processing.keyframe_detector import KeyFrameDetector
from time import sleep
import cv2

class IngestionController():
    
    def __init__(self):
        self.isStarted = False
        self.ingested_files_out_dir = "/app/edge_shared_files/process_data"
        self.notingested_files_out_dir = "/app/edge_shared_files/notprocessed_data"
        self.allowedIngestFileExtensions = [".jpg",".tiff", ".jpeg", ".img"]
        self.keyframe_extractor = KeyFrameDetector()
        self.factory = IngressFactory()
        self.threads = []

    def stage_file_for_process(self, img):
       print(f"Start Staging of {img}")
       if (not os.path.exists(self.ingested_files_out_dir)):
            os.mkdir(self.ingested_files_out_dir)

       file_name, file_extension = fileUtils.get_filename_and_extension(img)

       if (file_extension not in self.allowedIngestFileExtensions):
            return
       
       staged_file = os.path.join(self.ingested_files_out_dir, os.path.basename(file_name) + file_extension)
       shutil.move(img, staged_file)
       print(f"Staged to Staging of {staged_file}")

    def move_file_to_unprocessed(self, img):
       print(f"Start Staging of {img}")
       if (not os.path.exists(self.notingested_files_out_dir)):
            os.mkdir(self.notingested_files_out_dir)

       file_name, file_extension = fileUtils.get_filename_and_extension(img)

       if (file_extension not in self.allowedIngestFileExtensions):
            return
       
       unprocessed_file = os.path.join(self.notingested_files_out_dir, os.path.basename(file_name) + file_extension)
       shutil.move(img, unprocessed_file)
       print(f"Staged to Staging of {unprocessed_file}")


    def start(self):
        self.isStarted = True
        print("Edge Controller Started.")
        for ingestionProvider in self.__getIngestionTypesFromConfiguration():
             print(type(ingestionProvider))
             sleep(5)
             ingestion_thread = threading.Thread(target= self.__readData, args = (ingestionProvider,))
             self.threads.append(ingestion_thread)
             ingestion_thread.start()


    def stop(self):
         print("Edge Controller Ending silently.")
         self.isStarted = False
         for thread in self.threads:
             thread.join()

    def __getIngestionTypesFromConfiguration(self):
        ingestionTypeProviders = []
        ingress_configuration_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "configurations", "ingress_configuration.json") 
        data = fileUtils.read_json(ingress_configuration_path)
        available_cfgs = data["ingress_configurations"]
        for cfg in available_cfgs:
            if cfg["active"]:
                ingressModeFromConfig = EdgeDataIngressMode[cfg["mode"]]
                ingressModeParametersFromConfig = cfg["parameters"]
                ingestionTypeProvider = self.factory.create(ingressModeFromConfig, ingressModeParametersFromConfig)
                ingestionTypeProviders.append(ingestionTypeProvider)
        print("Ingestion providers found:" + str(len(ingestionTypeProviders)))
        sleep(5)
        return ingestionTypeProviders
    
    def __detectIfImageIsKeyFrame(self, previous_image, current_image, algorithm="PBT"):
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


    def __readData(self, ingressProvider:IngressionBase):
        keyframe_images = []
        non_keyframe_images = []

        while self.isStarted:
            try:
                print("Start Reading Data from Source")
                last_image = None
                ingressProvider.read()
                image = ingressProvider.getNextData()
                image_count = 0
                while image != None :
                    print(f"Ingress: Reading file {image}")
                    image_path = os.path.join(ingressProvider.input_dir, image)
                    print(f"Entering Keyframe Detector")
                    curr_img =  cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
                    print(last_image)
                    isKeyFrame = True if last_image == None else self.__detectIfImageIsKeyFrame(last_image, curr_img)
                    if isKeyFrame:
                        self.stage_file_for_process(image_path)
                    else:
                        self.move_file_to_unprocessed(image_path)

                    image_count = image_count + 1
                    
                    # if image_count == 5:
                    #    print("Partial keyframe processing>>>>>>>>>")
                    #    self.__removeNonKeyFrames(non_keyframe_images)
                    #    self.__stageKeyframes(keyframe_images)
                    #    image_count = 0
                       
                    last_image = curr_img.copy()
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





    




             