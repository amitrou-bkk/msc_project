from dataclasses import dataclass
from src.edge_layer.ingression_models.IngressionBase import DataIngressionConfiguration
import src.utilities.file as fileUtils
import os

class FileSystem(DataIngressionConfiguration):

    def __init__(self, config_file_path="configuration.json"):
        self.path = config_file_path
        self.input_dir = None
        self.staging_dir = None
        self.current_index = 0
        self.files = []

    def read(self):
        data = fileUtils.read_json(self.path)
        available_cfgs = data["ingress_configurations"]
        for cfg in available_cfgs:
            if cfg["mode"] == "FileSystem":
                self.input_dir = cfg["parameters"]["input_dir"]
                self.staging_dir = cfg["parameters"]["process_dir"]
                break
        self.files = os.listdir(self.input_dir)

    def getNextData(self):
        if len(self.files) == 0:
             return None
        if self.current_index >= len(self.files):
            self.current_index = 0 
            return None
        data = self.files[self.current_index]
        self.current_index =  self.current_index + 1 
        return data