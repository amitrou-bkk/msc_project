from dataclasses import dataclass
from utilities.file import read_json
from edge_layer.ingression_models.DataIngressionConfiguration import DataIngressionConfiguration

class FileSystem(DataIngressionConfiguration):

    def __init__(self):
        self.input_dir = None
        self.staging_dir = None

    def read(self):
           data = read_json("configuration.json")
           self.input_dir = data["properties"]["input_dir"]
           self.staging_dir = data["properties"]["input_dir"]