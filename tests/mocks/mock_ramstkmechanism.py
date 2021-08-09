# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKMechanism(MockRAMSTKBaseRecord):
    __defaults__ = {
        "description": "",
        "pof_include": 1,
        "rpn": 0,
        "rpn_detection": 10,
        "rpn_detection_new": 10,
        "rpn_new": 0,
        "rpn_occurrence": 10,
        "rpn_occurrence_new": 10,
    }

    def __init__(self):
        self.revision_id = 0
        self.hardware_id = 0
        self.mode_id = 0
        self.mechanism_id = 0
        self.description = self.__defaults__["description"]
        self.pof_include = self.__defaults__["pof_include"]
        self.rpn = self.__defaults__["rpn"]
        self.rpn_detection = self.__defaults__["rpn_detection"]
        self.rpn_detection_new = self.__defaults__["rpn_detection_new"]
        self.rpn_new = self.__defaults__["rpn_new"]
        self.rpn_occurrence = self.__defaults__["rpn_occurrence"]
        self.rpn_occurrence_new = self.__defaults__["rpn_occurrence_new"]

        self.is_mode = False
        self.is_mechanism = True
        self.is_cause = False
        self.is_control = False
        self.is_action = False
        self.is_opload = False
        self.is_opstress = False
        self.is_testmethod = False

    def get_attributes(self):
        _attributes = {
            "mode_id": self.mode_id,
            "mechanism_id": self.mechanism_id,
            "description": self.description,
            "pof_include": self.pof_include,
            "rpn": self.rpn,
            "rpn_detection": self.rpn_detection,
            "rpn_detection_new": self.rpn_detection_new,
            "rpn_new": self.rpn_new,
            "rpn_occurrence": self.rpn_occurrence,
            "rpn_occurrence_new": self.rpn_occurrence_new,
        }

        return _attributes
