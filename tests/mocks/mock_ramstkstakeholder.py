# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKStakeholder(MockRAMSTKBaseTable):
    __defaults__ = {
        "customer_rank": 1,
        "description": "Stakeholder Input",
        "group": "",
        "improvement": 0.0,
        "overall_weight": 0.0,
        "planned_rank": 1,
        "priority": 1,
        "requirement_id": 0,
        "stakeholder": "",
        "user_float_1": 1.0,
        "user_float_2": 1.0,
        "user_float_3": 1.0,
        "user_float_4": 1.0,
        "user_float_5": 1.0,
    }

    def __init__(self):
        self.revision_id = 0
        self.stakeholder_id = 0
        self.customer_rank = self.__defaults__["customer_rank"]
        self.description = self.__defaults__["description"]
        self.group = self.__defaults__["group"]
        self.improvement = self.__defaults__["improvement"]
        self.overall_weight = self.__defaults__["overall_weight"]
        self.planned_rank = self.__defaults__["planned_rank"]
        self.priority = self.__defaults__["priority"]
        self.requirement_id = self.__defaults__["requirement_id"]
        self.stakeholder = self.__defaults__["stakeholder"]
        self.user_float_1 = self.__defaults__["user_float_1"]
        self.user_float_2 = self.__defaults__["user_float_2"]
        self.user_float_3 = self.__defaults__["user_float_3"]
        self.user_float_4 = self.__defaults__["user_float_4"]
        self.user_float_5 = self.__defaults__["user_float_5"]

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "stakeholder_id": self.stakeholder_id,
            "customer_rank": self.customer_rank,
            "description": self.description,
            "group": self.group,
            "improvement": self.improvement,
            "overall_weight": self.overall_weight,
            "planned_rank": self.planned_rank,
            "priority": self.priority,
            "requirement_id": self.requirement_id,
            "stakeholder": self.stakeholder,
            "user_float_1": self.user_float_1,
            "user_float_2": self.user_float_2,
            "user_float_3": self.user_float_3,
            "user_float_4": self.user_float_4,
            "user_float_5": self.user_float_5,
        }

        return _attributes
