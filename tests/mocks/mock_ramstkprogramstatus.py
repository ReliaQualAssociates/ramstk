# Standard Library Imports
from datetime import date

# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKProgramStatus(MockRAMSTKBaseTable):
    __defaults__ = {
        "cost_remaining": 0.0,
        "date_status": date.today(),
        "time_remaining": 0.0,
    }

    def __init__(self):
        self.revision_id = 0
        self.status_id = 0
        self.cost_remaining = self.__defaults__["cost_remaining"]
        self.date_status = self.__defaults__["date_status"]
        self.time_remaining = self.__defaults__["time_remaining"]

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "status_id": self.status_id,
            "cost_remaining": self.cost_remaining,
            "date_status": self.date_status,
            "time_remaining": self.time_remaining,
        }

        return _attributes
