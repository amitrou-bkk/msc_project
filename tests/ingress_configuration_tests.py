import unittest
import os
from src.edge_layer.ingression_models.IngressionFileSystem import FileSystem

class FileSystemConfiguratio_Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        test_config_file = os.path.join(os.path.dirname(__file__), "configuration-test.json")
        self.file_system_confinguration = FileSystem(config_file_path= test_config_file)
        self.config_data = self.file_system_confinguration.read()

    def test_is_filesystem_enabled(self):
        input_dir = self.file_system_confinguration.input_dir
        self.assertTrue(input_dir == "")
    
if __name__ == '__main__':
    unittest.main()