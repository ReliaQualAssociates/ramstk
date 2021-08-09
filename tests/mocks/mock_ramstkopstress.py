# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKOpStress(MockRAMSTKBaseRecord):
    __defaults__ = {
        "description": "",
        "load_history": "",
        "measurable_parameter": "",
        "remarks": "",
    }

    def __init__(self):
        self.revision_id = 0
        self.hardware_id = 0
        self.mode_id = 0
        self.mechanism_id = 0
        self.load_id = 0
        self.stress_id = 0
        self.description = self.__defaults__["description"]
        self.load_history = self.__defaults__["load_history"]
        self.measurable_parameter = self.__defaults__["measurable_parameter"]
        self.remarks = self.__defaults__["remarks"]

        self.is_mode = False
        self.is_mechanism = False
        self.is_opload = False
        self.is_opstress = True
        self.is_testmethod = False

    def get_attributes(self):
        _attributes = {
            "load_id": self.load_id,
            "stress_id": self.stress_id,
            "description": self.description,
            "load_history": self.load_history,
            "measurable_parameter": self.measurable_parameter,
            "remarks": self.remarks,
        }

        return _attributes
