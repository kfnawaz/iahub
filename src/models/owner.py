
import uuid
import datetime
from src.common.database import Database
from src.models.model import Model

class Owner(Model):

    collection = 'owner'

    def __init__(self, automation_id, owner_type, owner_id, created_date=datetime.datetime.utcnow(), _id=None):
        super().__init__()
        self.automation_id  = automation_id
        self.owner_type     = owner_type
        self.owner_id       = owner_id
        self.created_date   = created_date
        self._id          = _id or uuid.uuid4().hex


    def json(self):
        return {
            '_id' : self._id,
            'automation_id' : self.automation_id,
            'owner_type'    : self.owner_type,
            'owner_id'      : self.owner_id,
            'created_date'  : self.created_date
        }

    @classmethod
    def get_by_db_id(cls, db_id):
        return cls.get_by_id(db_id)

    @classmethod
    def get_by_automation_id(cls, automation_id):
        return cls.find_many_by('automation_id', automation_id)

    @classmethod
    def get_by_owner_id(cls, owner_id):
        return cls.find_many_by('owner_id', owner_id)

    @classmethod
    def get_by_owner_type(cls, owner_type):
        return cls.find_many_by('owner_type', owner_type)

