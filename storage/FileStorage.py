from src.storage.BaseStorage import BaseStorage
import os

class FileStorage(BaseStorage):
    def create_directory(self, path):
        try:
            os.mkdir(path)
        except Exception as ex:
            print(f"Directory {path} could not be created")
            print(f"Error {str(ex)}")

    def read_directory(self, path):
        return [os.path.join(path, file) for file in os.listdir(path)]
    
    def write_file(self, path):
        with open(path, "w") as f:
            f.write(path)

    def path_exists(self, path):
        return os.path.exists(path)

    def read_file(self, file):
        return file
    

        
