
import os
import shutil
import src.edge_layer.ingression_mode as IngressMode
from src.edge_layer.ingression_models.ingress_factory import IngressFactory
from time import sleep

class EdgeController():
    
    def __init__(self, ingress_mode: IngressMode):

        self.processed_files = []
        self.isStarted = False
        self.ingressProvider = IngressFactory().create(ingress_mode)
        self.input_dir = ""
        self.process_dir = ""

    def getFileWithoutExtension(self, filename):
        os.path.splitext(filename)[0]

    def process_files(self):
       arr = os.listdir()
       for file in arr:
            if file not in self.process_files:
                staged_file = os.path.join(self.process_dir, self.getFileWithoutExtension(file), ".img")
                shutil.move(file,  staged_file)
                self.processed_files.append(file)

    def startListening(self):
        self.isStarted = True
        print("Edge Controller Started.")
        while self.isStarted:
            print("Start Reading Data from Source")
            self.ingressProvider.read()
            while image := self.ingressProvider.getNextData():
                print(image)
            print("Finished Reading Data.")
            sleep(1)

    def stopListening(self):
         print("Edge Controller Ending silently.")
         self.isStarted = False

    




             