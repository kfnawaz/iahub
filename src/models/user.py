__author__='nawaz'

import uuid
import datetime
from typing import Dict
from flask import session
from src.models.process import Process
from src.models.automation import Automation
from src.models.owner import Owner
from src.models.asset import Asset
from src.models.model import Model
import src.models.errors as UserErrors
from src.common.utils import Utils


class User(Model):

    collection = 'users'

    def __init__(self, email, password, _id=None):
        super().__init__()
        self.email      = email
        self.password   = password
        self._id        =  _id or uuid.uuid4().hex

    @classmethod
    def get_by_email(cls, email) -> "User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this email as not found.')

    @classmethod
    def get_by_user_id(cls, user_id):
        user = cls.find_one_by('_id', user_id)
        if user is not None: return user



    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            if not Utils.check_hashed_password(password, user.password):
                raise UserErrors.IncorrectPasswordError('Your password was incorrect')
            return True
        return False



    @classmethod
    def register(cls, email, password) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('The email does not have the right format.')
        try:
            cls.get_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError('The email you used to register already exits.')
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_db()
        return True



    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email



    @staticmethod
    def logout():
        session['email'] = None


    @staticmethod
    def get_all_processes():
        return Process.get_all()

    @staticmethod
    def get_all_automations():
        return Automation.get_all()

    @staticmethod
    def get_all_owners():
        return Owner.get_all()


    def create_new_process(self, lob, group, process_name, process_desc, created_date=datetime.datetime.utcnow()):
        process = Process(lob=lob,
                          group=group,
                          process_name=process_name,
                          process_desc=process_desc,
                          created_date=created_date)
        process.save_to_db()


    def json(self) -> Dict:
        return {
            "email" : self.email,
            "_id" : self._id,
            "password" : self.password
        }

