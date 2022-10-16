import os
import src.edge_layer.ingression_mode as inMode
import src.edge_layer.ingression_models.IngressionFileSystem as IngressFs

class IngressFactory():
    def create(self, edgeDataIngressMode):
        if (edgeDataIngressMode == inMode.EdgeDataIngressMode.FileSystem):
            return IngressFs.FileSystem(config_file_path = os.path.join(os.path.dirname(__file__), "configuration.json"))
        else:
            return None