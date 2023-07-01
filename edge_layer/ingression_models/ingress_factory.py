import os
import src.edge_layer.ingression_mode as inMode
import src.edge_layer.ingression_models.IngressionFileSystem as IngressFs

class IngressFactory():
    def create(self, edgeDataIngressMode, parameters):
        if (edgeDataIngressMode == "FileSystem"):
            if parameters == None:
                raise Exception("Parameters were not provided")
            if "input_dir" not in parameters:
                raise Exception("input_dir parameter not found")
            return IngressFs.FileSystem(parameters["input_dir"])
        else:
            return None