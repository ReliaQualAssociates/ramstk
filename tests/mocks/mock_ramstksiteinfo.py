# Standard Library Imports
from datetime import date, timedelta

# RAMSTK Local Imports
from . import MockRAMSTKBaseTable


class MockRAMSTKSiteInfo(MockRAMSTKBaseTable):
    __defaults__ = {
        "site_name": "",
        "product_key": "",
        "expire_on": date.today() + timedelta(30),
        "function_enabled": 0,
        "requirement_enabled": 0,
        "hardware_enabled": 0,
        "software_enabled": 0,
        "rcm_enabled": 0,
        "testing_enabled": 0,
        "incident_enabled": 0,
        "survival_enabled": 0,
        "vandv_enabled": 0,
        "hazard_enabled": 0,
        "stakeholder_enabled": 0,
        "allocation_enabled": 0,
        "similar_item_enabled": 0,
        "fmea_enabled": 0,
        "pof_enabled": 0,
        "rbd_enabled": 0,
        "fta_enabled": 0,
    }

    def __init__(self):
        self.site_id = 0
        self.site_name = self.__defaults__["site_name"]
        self.product_key = self.__defaults__["product_key"]
        self.expire_on = self.__defaults__["expire_on"]
        self.function_enabled = self.__defaults__["function_enabled"]
        self.requirement_enabled = self.__defaults__["requirement_enabled"]
        self.hardware_enabled = self.__defaults__["hardware_enabled"]
        self.software_enabled = self.__defaults__["software_enabled"]
        self.rcm_enabled = self.__defaults__["rcm_enabled"]
        self.testing_enabled = self.__defaults__["testing_enabled"]
        self.incident_enabled = self.__defaults__["incident_enabled"]
        self.survival_enabled = self.__defaults__["survival_enabled"]
        self.vandv_enabled = self.__defaults__["vandv_enabled"]
        self.hazard_enabled = self.__defaults__["hazard_enabled"]
        self.stakeholder_enabled = self.__defaults__["stakeholder_enabled"]
        self.allocation_enabled = self.__defaults__["allocation_enabled"]
        self.similar_item_enabled = self.__defaults__["similar_item_enabled"]
        self.fmea_enabled = self.__defaults__["fmea_enabled"]
        self.pof_enabled = self.__defaults__["pof_enabled"]
        self.rbd_enabled = self.__defaults__["rbd_enabled"]
        self.fta_enabled = self.__defaults__["fta_enabled"]

    def get_attributes(self):
        _attributes = {
            "site_id": self.site_id,
            "site_name": self.site_name,
            "product_key": self.product_key,
            "expire_on": self.expire_on,
            "function_enabled": self.function_enabled,
            "requirement_enabled": self.requirement_enabled,
            "hardware_enabled": self.hardware_enabled,
            "software_enabled": self.software_enabled,
            "rcm_enabled": self.rcm_enabled,
            "testing_enabled": self.testing_enabled,
            "incident_enabled": self.incident_enabled,
            "survival_enabled": self.survival_enabled,
            "vandv_enabled": self.vandv_enabled,
            "hazard_enabled": self.hazard_enabled,
            "stakeholder_enabled": self.stakeholder_enabled,
            "allocation_enabled": self.allocation_enabled,
            "similar_item_enabled": self.similar_item_enabled,
            "fmea_enabled": self.fmea_enabled,
            "pof_enabled": self.pof_enabled,
            "rbd_enabled": self.rbd_enabled,
            "fta_enabled": self.fta_enabled,
        }

        return _attributes
