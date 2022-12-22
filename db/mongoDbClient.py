
from src.db.dbClient import DbClient

from pymongo import MongoClient

class MongoDbClient(DbClient):
    def __init__(self, host, db_name, port, username, password):
        super().__init__(host, db_name, port, username, password)
        self.client = MongoClient(f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/')
        self.db_name = db_name
        
    def connect(self):
        try:
            print(self.client.server_info())
            return True
        except Exception as exception:
            print(exception)
            return False

    def createDb(self, name):
        dblist = self.client.list_database_names()
        self.db_name = name

        if name in dblist:
            print(f"{name} database exists.")
            return

        self.db = self.client[name]
        self.collection = self.db["defaultCollection"]
        dummy_doc = self.collection.insert_one({})
        return dummy_doc.inserted_id

    def add_document(self, data):
        if type(data) is dict:
            self.db = self.client[self.db_name]
            self.collection = self.db["defaultCollection"]
            self.collection.insert_one(data)
        else:
            raise Exception("Data were not in dictionary format")

        