# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKControl(MockRAMSTKBaseRecord):
    __defaults__ = {"description": "", "type_id": ""}

    def __init__(self):
        self.revision_id = 0
        self.hardware_id = 0
        self.mode_id = 0
        self.mechanism_id = 0
        self.cause_id = 0
        self.control_id = 0
        self.description = self.__defaults__["description"]
        self.type_id = self.__defaults__["type_id"]

        self.is_mode = False
        self.is_mechanism = False
        self.is_cause = False
        self.is_control = True
        self.is_action = False

    def get_attributes(self):
        _attributes = {
            "cause_id": self.cause_id,
            "control_id": self.control_id,
            "description": self.description,
            "type_id": self.type_id,
        }

        return _attributes
