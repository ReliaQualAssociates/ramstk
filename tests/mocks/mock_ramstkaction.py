# Standard Library Imports
from datetime import date, timedelta

# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKAction(MockRAMSTKBaseRecord):
    __defaults__ = {
        "action_recommended": "",
        "action_category": "",
        "action_owner": "",
        "action_due_date": date.today() + timedelta(days=30),
        "action_status": "",
        "action_taken": "",
        "action_approved": 0,
        "action_approve_date": date.today() + timedelta(days=30),
        "action_closed": 0,
        "action_close_date": date.today() + timedelta(days=30),
    }

    def __init__(self):
        self.revision_id = 0
        self.hardware_id = 0
        self.mode_id = 0
        self.mechanism_id = 0
        self.cause_id = 0
        self.action_id = 0
        self.action_recommended = self.__defaults__["action_recommended"]
        self.action_category = self.__defaults__["action_category"]
        self.action_owner = self.__defaults__["action_owner"]
        self.action_due_date = self.__defaults__["action_due_date"]
        self.action_status = self.__defaults__["action_status"]
        self.action_taken = self.__defaults__["action_taken"]
        self.action_approved = self.__defaults__["action_approved"]
        self.action_approve_date = self.__defaults__["action_approve_date"]
        self.action_closed = self.__defaults__["action_closed"]
        self.action_close_date = self.__defaults__["action_close_date"]

        self.is_mode = False
        self.is_mechanism = False
        self.is_cause = False
        self.is_control = False
        self.is_action = True

    def get_attributes(self):
        _attributes = {
            "cause_id": self.cause_id,
            "action_id": self.action_id,
            "action_recommended": self.action_recommended,
            "action_category": self.action_category,
            "action_owner": self.action_owner,
            "action_due_date": self.action_due_date,
            "action_status": self.action_status,
            "action_taken": self.action_taken,
            "action_approved": self.action_approved,
            "action_approve_date": self.action_approve_date,
            "action_closed": self.action_closed,
            "action_close_date": self.action_close_date,
        }

        return _attributes
