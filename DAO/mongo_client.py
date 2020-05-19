import ssl

from pymongo import MongoClient
from bson.json_util import dumps
from settings import MONGO_DB_CONNECTION,MONGO_DB_PIPELINE

class MongoDBClient:

    client = MongoClient(MONGO_DB_CONNECTION,ssl_cert_reqs=ssl.CERT_NONE)

    def get_database(self, database_name='user_db'):
        return self.client[database_name]

    def insert_documents(self, dataset, collection):
        db = self.get_database()
        collection = db[collection]
        inserted_ids = collection.insert_many(dataset).inserted_ids
        return inserted_ids

    def drop_collection(self,collection):
        db = self.get_database()
        db.drop_collection(collection)

    def get_books_with_user(self,collection = 'book_collection'):
        db = self.get_database()
        collection = db[collection]
        res = []
        cursor = collection.aggregate(MONGO_DB_PIPELINE)
        for cur in cursor:
            res .append(cur)
        return res

    def get_all_books(self, collection='book_collection'):
        db = self.get_database()
        collection = db[collection]
        res = []
        cursor = collection.find()
        for cur in cursor:
            res.append(cur)
        return res

    def get_all_users(self, collection='user_collection'):
        db = self.get_database()
        collection = db[collection]
        res = []
        cursor = collection.find()
        for cur in cursor:
            res.append(cur)
        return res

    def get_all_ratings(self, collection='ratings_collection'):
        db = self.get_database()
        collection = db[collection]
        res = []
        cursor = collection.find()
        for cur in cursor:
            res.append(cur)
        return res