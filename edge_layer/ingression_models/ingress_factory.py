import os
from src.edge_layer.ingression_models.ingression_mode import EdgeDataIngressMode 
import src.edge_layer.ingression_models.IngressionFileSystem as IngressFs

class IngressFactory():
    def create(self, edgeDataIngressMode: EdgeDataIngressMode, parameters):
        if (edgeDataIngressMode == EdgeDataIngressMode.FileSystem):
            if parameters == None:
                raise Exception("Parameters were not provided")
            if "input_dir" not in parameters:
                raise Exception("input_dir parameter not found")
            return IngressFs.FileSystem(parameters["input_dir"])
        else:
           raise Exception("Not a supported ingress mode")