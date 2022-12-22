from abc import ABC, abstractmethod

class BaseStorage(ABC):
   @abstractmethod
   def create_directory(self, path):
        pass

   @abstractmethod
   def read_directory(self, path):
        pass

   @abstractmethod
   def write_file(self, path, data):
        pass

   @abstractmethod
   def path_exists(self, path):
        pass

   @abstractmethod
   def read_file(self, file):
        pass
