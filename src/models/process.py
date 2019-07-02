
import uuid
import datetime
from src.models.automation import Automation
from src.models.model import Model

class Process(Model):

    collection = 'process'

    def __init__(self, lob, group, process_name, process_desc, user=None, created_by=None, created_date=None, updated_by=None, updated_date=None, _id=None):
        super().__init__()
        self.lob          = lob
        self.group        = group
        self.process_name = process_name
        self.process_desc = process_desc
        self.user         = user
        self.created_by   = created_by
        self.created_date = created_date
        self.updated_by   = updated_by
        self.updated_date = updated_date
        self._id          = _id or uuid.uuid4().hex
        #created_date=datetime.datetime.utcnow(),


    def json(self):
        return {
            '_id'          : self._id,
            'lob'          : self.lob,
            'group'        : self.group,
            'process_name' : self.process_name,
            'process_desc' : self.process_desc,
            'created_by'   : self.created_by,
            'created_date' : self.created_date,
            'updated_by'   : self.updated_by,
            'updated_date' : self.updated_date
        }


    def new_automation(self, automation_tag, automation_name, platform, golive_dt, status, retirement_dt, last_certified_dt, created_date=datetime.datetime.utcnow(), _id=None):
        automation = Automation(automation_tag       = automation_tag,
                                automation_name     = automation_name,
                                platform            = platform,
                                golive_dt           = golive_dt,
                                status              = status,
                                retirement_dt       = retirement_dt,
                                last_certified_dt   = last_certified_dt,
                                created_date        = created_date,
                                process_id          = self._id)
        automation.save_to_db()


    def get_automations(self):
        return Automation.find_many_by('process_id', self._id)



