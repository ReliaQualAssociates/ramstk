# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKTestMethod(MockRAMSTKBaseTable):
    __defaults__ = {"description": "", "boundary_conditions": "", "remarks": ""}

    def __init__(self):
        self.revision_id = 0
        self.hardware_id = 0
        self.mode_id = 0
        self.mechanism_id = 0
        self.load_id = 0
        self.test_id = 0
        self.description = self.__defaults__["description"]
        self.boundary_conditions = self.__defaults__["boundary_conditions"]
        self.remarks = self.__defaults__["remarks"]

        self.is_mode = False
        self.is_mechanism = False
        self.is_opload = False
        self.is_opstress = False
        self.is_testmethod = True

    def get_attributes(self):
        _attributes = {
            "load_id": self.load_id,
            "test_id": self.test_id,
            "description": self.description,
            "boundary_conditions": self.boundary_conditions,
            "remarks": self.remarks,
        }

        return _attributes
