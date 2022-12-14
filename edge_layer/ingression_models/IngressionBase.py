import abc
from abc import ABC, abstractmethod

class DataIngressionConfiguration(ABC):
    
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def getNextData(self):
        pass
    