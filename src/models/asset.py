from typing import Dict, List
import uuid
import datetime
from src.common.database import Database
from src.models.model import Model

class Asset(Model):

    collection = 'asset'

    def __init__(self, automation_id, asset_type, asset_name, created_date=datetime.datetime.utcnow(), _id=None):
        super().__init__()
        self.automation_id  = automation_id
        self.asset_type     = asset_type
        self.asset_name     = asset_name
        self.created_date   = created_date
        self._id            = _id or uuid.uuid4().hex


    def json(self) -> Dict:
        return {
            '_id' : self._id,
            'automation_id' : self.automation_id,
            'asset_type'    : self.asset_type,
            'asset_name'    : self.asset_name,
            'created_date'  : self.created_date
        }


    @classmethod
    def get_by_dbid(cls, dbid):
        return cls.find_one_by('_id', dbid)


    @classmethod
    def get_by_automation_id(cls, automation_id) -> List:
        return cls.find_many_by('automation_id', automation_id)


    @classmethod
    def get_by_asset_id(cls, asset_id) -> List:
        return cls.find_many_by('asset_id', asset_id)


    @classmethod
    def get_by_asset_type(cls, asset_type) -> List:
        cls.find_many_by('asset_type', asset_type)

