
import os
import shutil
import threading
import src.edge_layer.ingression_mode as IngressMode
from src.edge_layer.ingression_models.IngressionBase import DataIngressionConfiguration
from src.edge_layer.ingression_models.ingress_factory import IngressFactory
import src.utilities.file as fileUtils
from time import sleep

class IngestionController():
    
    def __init__(self):
        self.isStarted = False
        self.process_dir = "/app/edge_shared_files/process_data"
        self.allowedExtensions = [".jpg",".tiff", ".jpeg", ".img"]

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
    
    def __readData(self, ingressProvider:DataIngressionConfiguration):
        while self.isStarted:
            try:
                print("Start Reading Data from Source")
                ingressProvider.read()
                image = ingressProvider.getNextData()
                while image != None :
                    print(f"Ingress: Reading file {image}")
                    image_path = os.path.join(ingressProvider.input_dir, image)
                    self.stage_file_for_process(image_path)
                    image = ingressProvider.getNextData()
                    print("Finished Reading Data.")
                sleep(2)
            except Exception as ex:
                print(ex)
    




             