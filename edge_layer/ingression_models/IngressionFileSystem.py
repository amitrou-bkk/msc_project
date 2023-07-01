from dataclasses import dataclass
from src.edge_layer.ingression_models.IngressionBase import DataIngressionConfiguration
import src.utilities.file as fileUtils
import os

class FileSystem(DataIngressionConfiguration):

    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.current_index = 0
        self.files = []

    def read(self):
        self.files = os.listdir(self.input_dir)
        print(self.files)

    def getNextData(self):
        print("getNextData")
        if len(self.files) == 0:
             return None
        if self.current_index >= len(self.files):
            self.current_index = 0 
            return None
        data = self.files[self.current_index]
        self.current_index =  self.current_index + 1 
        return data