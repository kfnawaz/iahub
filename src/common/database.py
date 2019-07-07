from typing import Dict
import pymongo
import os


class Database(object):

    #URI = "mongodb://127.0.0.1:27017"
    #URI = "mongodb://<dbuser>:<dbpassword>@ds139072.mlab.com:39072/heroku_qd4lr870"
    URI = os.environ.get("MONGOLAB_URI")
    DATABASE = None


    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['iahubdb']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        return Database.DATABASE[collection].update(query, data)
        #return Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> None:
        return Database.DATABASE[collection].remove(query)
