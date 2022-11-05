import unittest
from src.db.mongoDbClient import MongoDbClient

class MongoDb_Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = MongoDbClient("localhost", "", 27017, "root", "example")
        
    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_connection(self): 
        self.client.connect()
        self.assertEqual(1,1)

    def test_connection(self): 
        dummy_created_doc_id = self.client.createDb("test-db")
        self.assertIsNotNone(dummy_created_doc_id)

if __name__ == '__main__':
    unittest.main()