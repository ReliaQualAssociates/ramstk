# Standard Library Imports
from datetime import date

# RAMSTK Package Imports
from ramstk.utilities import none_to_default

# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKRequirement(MockRAMSTKBaseTable):
    __defaults__ = {
        "derived": 0,
        "description": "",
        "figure_number": "",
        "owner": 0,
        "page_number": "",
        "parent_id": 0,
        "priority": 0,
        "requirement_code": "",
        "specification": "",
        "requirement_type": 0,
        "validated": 0,
        "validated_date": date.today(),
        "q_clarity_0": 0,
        "q_clarity_1": 0,
        "q_clarity_2": 0,
        "q_clarity_3": 0,
        "q_clarity_4": 0,
        "q_clarity_5": 0,
        "q_clarity_6": 0,
        "q_clarity_7": 0,
        "q_clarity_8": 0,
        "q_complete_0": 0,
        "q_complete_1": 0,
        "q_complete_2": 0,
        "q_complete_3": 0,
        "q_complete_4": 0,
        "q_complete_5": 0,
        "q_complete_6": 0,
        "q_complete_7": 0,
        "q_complete_8": 0,
        "q_complete_9": 0,
        "q_consistent_0": 0,
        "q_consistent_1": 0,
        "q_consistent_2": 0,
        "q_consistent_3": 0,
        "q_consistent_4": 0,
        "q_consistent_5": 0,
        "q_consistent_6": 0,
        "q_consistent_7": 0,
        "q_consistent_8": 0,
        "q_verifiable_0": 0,
        "q_verifiable_1": 0,
        "q_verifiable_2": 0,
        "q_verifiable_3": 0,
        "q_verifiable_4": 0,
        "q_verifiable_5": 0,
    }

    def __init__(self):
        self.revision_id = 0
        self.requirement_id = 0
        self.derived = self.__defaults__["derived"]
        self.description = self.__defaults__["description"]
        self.figure_number = self.__defaults__["figure_number"]
        self.owner = self.__defaults__["owner"]
        self.page_number = self.__defaults__["page_number"]
        self.parent_id = self.__defaults__["parent_id"]
        self.priority = self.__defaults__["priority"]
        self.requirement_code = self.__defaults__["requirement_code"]
        self.specification = self.__defaults__["specification"]
        self.requirement_type = self.__defaults__["requirement_type"]
        self.validated = self.__defaults__["validated"]
        self.validated_date = self.__defaults__["validated_date"]
        self.q_clarity_0 = self.__defaults__["q_clarity_0"]
        self.q_clarity_1 = self.__defaults__["q_clarity_1"]
        self.q_clarity_2 = self.__defaults__["q_clarity_2"]
        self.q_clarity_3 = self.__defaults__["q_clarity_3"]
        self.q_clarity_4 = self.__defaults__["q_clarity_4"]
        self.q_clarity_5 = self.__defaults__["q_clarity_5"]
        self.q_clarity_6 = self.__defaults__["q_clarity_6"]
        self.q_clarity_7 = self.__defaults__["q_clarity_7"]
        self.q_clarity_8 = self.__defaults__["q_clarity_8"]
        self.q_complete_0 = self.__defaults__["q_complete_0"]
        self.q_complete_1 = self.__defaults__["q_complete_1"]
        self.q_complete_2 = self.__defaults__["q_complete_2"]
        self.q_complete_3 = self.__defaults__["q_complete_3"]
        self.q_complete_4 = self.__defaults__["q_complete_4"]
        self.q_complete_5 = self.__defaults__["q_complete_5"]
        self.q_complete_6 = self.__defaults__["q_complete_6"]
        self.q_complete_7 = self.__defaults__["q_complete_7"]
        self.q_complete_8 = self.__defaults__["q_complete_8"]
        self.q_complete_9 = self.__defaults__["q_complete_9"]
        self.q_consistent_0 = self.__defaults__["q_consistent_0"]
        self.q_consistent_1 = self.__defaults__["q_consistent_1"]
        self.q_consistent_2 = self.__defaults__["q_consistent_2"]
        self.q_consistent_3 = self.__defaults__["q_consistent_3"]
        self.q_consistent_4 = self.__defaults__["q_consistent_4"]
        self.q_consistent_5 = self.__defaults__["q_consistent_5"]
        self.q_consistent_6 = self.__defaults__["q_consistent_6"]
        self.q_consistent_7 = self.__defaults__["q_consistent_7"]
        self.q_consistent_8 = self.__defaults__["q_consistent_8"]
        self.q_verifiable_0 = self.__defaults__["q_verifiable_0"]
        self.q_verifiable_1 = self.__defaults__["q_verifiable_1"]
        self.q_verifiable_2 = self.__defaults__["q_verifiable_2"]
        self.q_verifiable_3 = self.__defaults__["q_verifiable_3"]
        self.q_verifiable_4 = self.__defaults__["q_verifiable_4"]
        self.q_verifiable_5 = self.__defaults__["q_verifiable_5"]

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "requirement_id": self.requirement_id,
            "derived": self.derived,
            "description": self.description,
            "figure_number": self.figure_number,
            "owner": self.owner,
            "page_number": self.page_number,
            "parent_id": self.parent_id,
            "priority": self.priority,
            "requirement_code": self.requirement_code,
            "specification": self.specification,
            "requirement_type": self.requirement_type,
            "validated": self.validated,
            "validated_date": self.validated_date,
            "q_clarity_0": self.q_clarity_0,
            "q_clarity_1": self.q_clarity_1,
            "q_clarity_2": self.q_clarity_2,
            "q_clarity_3": self.q_clarity_3,
            "q_clarity_4": self.q_clarity_4,
            "q_clarity_5": self.q_clarity_5,
            "q_clarity_6": self.q_clarity_6,
            "q_clarity_7": self.q_clarity_7,
            "q_clarity_8": self.q_clarity_8,
            "q_complete_0": self.q_complete_0,
            "q_complete_1": self.q_complete_1,
            "q_complete_2": self.q_complete_2,
            "q_complete_3": self.q_complete_3,
            "q_complete_4": self.q_complete_4,
            "q_complete_5": self.q_complete_5,
            "q_complete_6": self.q_complete_6,
            "q_complete_7": self.q_complete_7,
            "q_complete_8": self.q_complete_8,
            "q_complete_9": self.q_complete_9,
            "q_consistent_0": self.q_consistent_0,
            "q_consistent_1": self.q_consistent_1,
            "q_consistent_2": self.q_consistent_2,
            "q_consistent_3": self.q_consistent_3,
            "q_consistent_4": self.q_consistent_4,
            "q_consistent_5": self.q_consistent_5,
            "q_consistent_6": self.q_consistent_6,
            "q_consistent_7": self.q_consistent_7,
            "q_consistent_8": self.q_consistent_8,
            "q_verifiable_0": self.q_verifiable_0,
            "q_verifiable_1": self.q_verifiable_1,
            "q_verifiable_2": self.q_verifiable_2,
            "q_verifiable_3": self.q_verifiable_3,
            "q_verifiable_4": self.q_verifiable_4,
            "q_verifiable_5": self.q_verifiable_5,
        }

        return _attributes

    def create_code(self, prefix: str) -> None:
        _zeds = 4 - len(str(self.requirement_id))
        _pad = "0" * _zeds
        _code = "{0:s}-{1:s}{2:d}".format(prefix, _pad, self.requirement_id)

        self.requirement_code = str(none_to_default(_code, ""))
