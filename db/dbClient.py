from abc import ABC, abstractmethod

class DbClient(ABC):
    def __init__(self, host, db_name, port, username, password):
       self.host = host
       self.db_name = db_name
       self.port = port
       self.username = username
       self.password = password
       
    @abstractmethod
    def connect():
        pass