# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKOpLoad(MockRAMSTKBaseTable):
    __defaults__ = {"description": "", "damage_model": "", "priority_id": 0}

    def __init__(self):
        self.revision_id = 0
        self.hardware_id = 0
        self.mode_id = 0
        self.mechanism_id = 0
        self.load_id = 0
        self.description = self.__defaults__["description"]
        self.damage_model = self.__defaults__["damage_model"]
        self.priority_id = self.__defaults__["priority_id"]

        self.is_mode = False
        self.is_mechanism = False
        self.is_opload = True
        self.is_opstress = False
        self.is_testmethod = False

    def get_attributes(self):
        _attributes = {
            "mechanism_id": self.mechanism_id,
            "load_id": self.load_id,
            "description": self.description,
            "damage_model": self.damage_model,
            "priority_id": self.priority_id,
        }

        return _attributes
