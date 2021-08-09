# Standard Library Imports
from datetime import date

# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKProgramInfo(MockRAMSTKBaseRecord):
    __defaults__ = {
        "function_active": 1,
        "requirement_active": 1,
        "hardware_active": 1,
        "software_active": 0,
        "rcm_active": 0,
        "testing_active": 0,
        "incident_active": 0,
        "survival_active": 0,
        "vandv_active": 1,
        "hazard_active": 1,
        "stakeholder_active": 1,
        "allocation_active": 1,
        "similar_item_active": 1,
        "fmea_active": 1,
        "pof_active": 1,
        "rbd_active": 0,
        "fta_active": 0,
        "created_on": date.today(),
        "created_by": "",
        "last_saved": date.today(),
        "last_saved_by": "",
    }

    def __init__(self):
        self.revision_id = 0
        self.function_active = self.__defaults__["function_active"]
        self.requirement_active = self.__defaults__["requirement_active"]
        self.hardware_active = self.__defaults__["hardware_active"]
        self.software_active = self.__defaults__["software_active"]
        self.rcm_active = self.__defaults__["rcm_active"]
        self.testing_active = self.__defaults__["testing_active"]
        self.incident_active = self.__defaults__["incident_active"]
        self.survival_active = self.__defaults__["survival_active"]
        self.vandv_active = self.__defaults__["vandv_active"]
        self.hazard_active = self.__defaults__["hazard_active"]
        self.stakeholder_active = self.__defaults__["stakeholder_active"]
        self.allocation_active = self.__defaults__["allocation_active"]
        self.similar_item_active = self.__defaults__["similar_item_active"]
        self.fmea_active = self.__defaults__["fmea_active"]
        self.pof_active = self.__defaults__["pof_active"]
        self.rbd_active = self.__defaults__["rbd_active"]
        self.fta_active = self.__defaults__["fta_active"]
        self.created_on = self.__defaults__["created_on"]
        self.created_by = self.__defaults__["created_by"]
        self.last_saved = self.__defaults__["last_saved"]
        self.last_saved_by = self.__defaults__["last_saved_by"]

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "function_active": self.function_active,
            "requirement_active": self.requirement_active,
            "hardware_active": self.hardware_active,
            "software_active": self.software_active,
            "rcm_active": self.rcm_active,
            "testing_active": self.testing_active,
            "incident_active": self.incident_active,
            "survival_active": self.survival_active,
            "vandv_active": self.vandv_active,
            "fmea_active": self.fmea_active,
            "pof_active": self.pof_active,
            "hazard_active": self.hazard_active,
            "stakeholder_active": self.stakeholder_active,
            "allocation_active": self.allocation_active,
            "similar_item_active": self.similar_item_active,
            "rbd_active": self.rbd_active,
            "fta_active": self.fta_active,
            "created_on": self.created_on,
            "created_by": self.created_by,
            "last_saved": self.last_saved,
            "last_saved_by": self.last_saved_by,
        }

        return _attributes
