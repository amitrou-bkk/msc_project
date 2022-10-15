
import os
import shutil
from time import sleep
class EdgeController():
    
    def __init__(self, ingress_mode):
        self.processed_files = []
        self.isStarted = False
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
            print("iteration passed")
            sleep(1)

    def stopListening(self):
         print("Edge Controller Ending silently.")
         self.isStarted = False

    




             