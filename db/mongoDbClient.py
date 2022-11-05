
from src.db.dbClient import DbClient

from pymongo import MongoClient

class MongoDbClient(DbClient):
    def __init__(self, host, db_name, port, username, password):
        super().__init__(host, db_name, port, username, password)
        self.client = MongoClient(f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/')
    
    def connect(self):
        print(self.client.server_info())
    
    def createDb(self, name):
        dblist = self.client.list_database_names()
        
        if name in dblist:
            print(f"{name} database exists.")
            return

        self.db = self.client[name]
        self.collection = self.db["defaultCollection"]
        dummy_doc = self.collection.insert_one({})
        return dummy_doc.inserted_id
        