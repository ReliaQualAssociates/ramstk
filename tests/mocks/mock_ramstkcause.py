# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKCause(MockRAMSTKBaseTable):
    __defaults__ = {
        "description": "",
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
        self.cause_id = 0
        self.description = self.__defaults__["description"]
        self.rpn = self.__defaults__["rpn"]
        self.rpn_detection = self.__defaults__["rpn_detection"]
        self.rpn_detection_new = self.__defaults__["rpn_detection_new"]
        self.rpn_new = self.__defaults__["rpn_new"]
        self.rpn_occurrence = self.__defaults__["rpn_occurrence"]
        self.rpn_occurrence_new = self.__defaults__["rpn_occurrence_new"]

        self.is_mode = False
        self.is_mechanism = False
        self.is_cause = True
        self.is_control = False
        self.is_action = False

    def get_attributes(self):
        _attributes = {
            "mode_id": self.mode_id,
            "mechanism_id": self.mechanism_id,
            "cause_id": self.cause_id,
            "description": self.description,
            "rpn": self.rpn,
            "rpn_detection": self.rpn_detection,
            "rpn_detection_new": self.rpn_detection_new,
            "rpn_new": self.rpn_new,
            "rpn_occurrence": self.rpn_occurrence,
            "rpn_occurrence_new": self.rpn_occurrence_new,
        }

        return _attributes
