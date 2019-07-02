import datetime
from abc import ABCMeta, abstractmethod
from src.common.database import Database


class Model(metaclass=ABCMeta):
    collection = "models"

    def __init__(self, *args, **kwargs):
        pass


    def insert(self):
        self.created_by = self.user
        self.created_date = datetime.datetime.utcnow()
        Database.insert(self.collection, self.json())


    def update(self):
        self.updated_by = self.user
        self.updated_date = datetime.datetime.utcnow()
        Database.update(self.collection, {"_id": self._id}, self.json())


    def remove_from_db(self):
        Database.remove(self.collection, {"_id": self._id})

    @abstractmethod
    def json(self):
        raise NotImplementedError

    @classmethod
    def get_by_id(cls, _id: str):
        return cls.find_one_by("_id", _id)

    @classmethod
    def get_all(cls):
        elements_from_db = Database.find(collection=cls.collection, query={})
        return [cls(**element) for element in elements_from_db]

    @classmethod
    def find_one_by(cls, attribute, value):
        return cls(**Database.find_one(collection=cls.collection, query={attribute: value}))

    @classmethod
    def find_many_by(cls, attribute, value):
        return [cls(**element) for element in Database.find(collection=cls.collection, query={attribute: value})]

