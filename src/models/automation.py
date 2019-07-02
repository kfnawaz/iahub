
import uuid
import datetime
from src.common.database import Database
from src.models.owner import Owner
from src.models.asset import Asset
from src.models.model import Model


class Automation(Model):

    collection = 'automation'

    def __init__(self,  process_id, automation_tag, automation_name, automation_desc, platform, golive_dt, status, retirement_dt, last_certified_dt,
                 user=None, created_by=None, created_date=None, updated_by=None, updated_date=None, _id=None):
        super().__init__()
        self.process_id         = process_id
        self.automation_tag     = automation_tag
        self.automation_name    = automation_name
        self.automation_desc    = automation_desc
        self.platform           = platform
        self.golive_dt          = golive_dt
        self.status             = status
        self.retirement_dt      = retirement_dt
        self.last_certified_dt  = last_certified_dt
        self.created_by         = created_by
        self.created_date       = created_date
        self.updated_by         = updated_by
        self.updated_date       = updated_date
        self.user               = user
        self._id                = _id or uuid.uuid4().hex



    def json(self):
        return {
            '_id'               : self._id,
            'process_id'        : self.process_id,
            'automation_tag'    : self.automation_tag,
            'automation_name'   : self.automation_name,
            'automation_desc'   : self.automation_desc,
            'platform'          : self.platform,
            'golive_dt'         : self.golive_dt,
            'status'            : self.status,
            'retirement_dt'     : self.retirement_dt,
            'last_certified_dt' : self.last_certified_dt,
            'created_date'      : self.created_date
        }



    def new_owner(self, owner_type, owner_id, created_date=datetime.datetime.utcnow()):
        owner = Owner(automation_id = self._id,
                      owner_type    = owner_type,
                      owner_id      = owner_id,
                      created_date  = created_date)
        owner.insert()


    def new_asset(self, asset_type, asset_name, created_date=datetime.datetime.utcnow()):
        asset = Asset(automation_id = self._id,
                      asset_type    = asset_type,
                      asset_name    = asset_name,
                      created_date  = created_date)
        asset.insert()


