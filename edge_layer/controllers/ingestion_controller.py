import os
import shutil
import threading
from src.edge_layer.ingression_models.ingression_mode import EdgeDataIngressMode
from src.edge_layer.ingression_models.IngressionBase import IngressionBase
from src.edge_layer.ingression_models.ingress_factory import IngressFactory
import src.utilities.file as fileUtils
from src.image_processing.keyframe_detector import KeyFrameDetector
from time import sleep

class IngestionController():
    
    def __init__(self):
        self.isStarted = False
        self.ingested_files_out_dir = "/app/edge_shared_files/process_data"
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
        data = fileUtils.read_json(os.path.join(os.path.dirname(__file__), "configuration.json"))
        available_cfgs = data["ingress_configurations"]
        for cfg in available_cfgs:
            if cfg["active"]:
                ingressModeFromConfig = EdgeDataIngressMode[cfg["mode"]]
                ingressModeFromConfig = cfg["parameters"]
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
                print("Leftovers>>>>>>>>>")
                print(keyframe_images)
                print(non_keyframe_images)
                print("Leftovers>>>>>>>>>")
                self.__removeNonKeyFrames(non_keyframe_images, 0) # tranfer leftovers
                self.__stageKeyframes(keyframe_images, 0) # tranfer leftovers

                last_image_path = None
                
                ingressProvider.read()
                image = ingressProvider.getNextData()
                image_count = 0
                while image != None :
                    print(f"Ingress: Reading file {image}")
                    image_path = os.path.join(ingressProvider.input_dir, image)
                    print(f"Entering Keyframe Detector")
                    isKeyFrame = self.__detectIfImageIsKeyFrame(last_image_path, image_path)
                    if isKeyFrame:
                        keyframe_images.append(image_path)
                    else:
                        non_keyframe_images.append(image_path)

                    image_count = image_count + 1
                    
                    if image_count == 5:
                       print("Partial keyframe processing>>>>>>>>>")
                       self.__removeNonKeyFrames(non_keyframe_images)
                       self.__stageKeyframes(keyframe_images)
                       image_count = 0
                       
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





    




             