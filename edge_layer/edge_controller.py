
import os
import shutil
import src.edge_layer.ingression_mode as IngressMode
from src.edge_layer.ingression_models.ingress_factory import IngressFactory
import src.utilities.file as fileUtils
from time import sleep

class EdgeController():
    
    def __init__(self, ingress_mode: IngressMode):

        self.processed_files = []
        self.isStarted = False
        self.ingressProvider = IngressFactory().create(ingress_mode)
        self.process_dir = "/app/edge_shared_files/process_data"
        self.allowedExtensions = [".jpg",".tiff", ".jpeg", ".img"]

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
        while self.isStarted:
            print("Start Reading Data from Source")
            self.ingressProvider.read()
            image = self.ingressProvider.getNextData()
            while image != None :
                print(f"Ingress: Reading file {image}")
                image_path = os.path.join(self.ingressProvider.input_dir, image)
                self.stage_file_for_process(image_path)
                image = self.ingressProvider.getNextData()
            print("Finished Reading Data.")
            sleep(2)

    def stopListening(self):
         print("Edge Controller Ending silently.")
         self.isStarted = False

    




             