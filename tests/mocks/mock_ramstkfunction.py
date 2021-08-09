# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKFunction(MockRAMSTKBaseRecord):
    __defaults__ = {
        "availability_logistics": 1.0,
        "availability_mission": 1.0,
        "cost": 0.0,
        "function_code": "Function Code",
        "hazard_rate_logistics": 0.0,
        "hazard_rate_mission": 0.0,
        "level": 0,
        "mmt": 0.0,
        "mcmt": 0.0,
        "mpmt": 0.0,
        "mtbf_logistics": 0.0,
        "mtbf_mission": 0.0,
        "mttr": 0.0,
        "name": "Function Name",
        "parent_id": 0,
        "remarks": "",
        "safety_critical": 0,
        "total_mode_count": 0,
        "total_part_count": 0,
        "type_id": 0,
    }

    def __init__(self):
        self.revision_id = 0
        self.function_id = 0
        self.availability_logistics = self.__defaults__["availability_logistics"]
        self.availability_mission = self.__defaults__["availability_mission"]
        self.cost = self.__defaults__["cost"]
        self.function_code = self.__defaults__["function_code"]
        self.hazard_rate_logistics = self.__defaults__["hazard_rate_logistics"]
        self.hazard_rate_mission = self.__defaults__["hazard_rate_mission"]
        self.level = self.__defaults__["level"]
        self.mmt = self.__defaults__["mmt"]
        self.mcmt = self.__defaults__["mcmt"]
        self.mpmt = self.__defaults__["mpmt"]
        self.mtbf_logistics = self.__defaults__["mtbf_logistics"]
        self.mtbf_mission = self.__defaults__["mtbf_mission"]
        self.mttr = self.__defaults__["mttr"]
        self.name = self.__defaults__["name"]
        self.parent_id = self.__defaults__["parent_id"]
        self.remarks = self.__defaults__["remarks"]
        self.safety_critical = self.__defaults__["safety_critical"]
        self.total_mode_count = self.__defaults__["total_mode_count"]
        self.total_part_count = self.__defaults__["total_part_count"]
        self.type_id = self.__defaults__["type_id"]

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "function_id": self.function_id,
            "availability_logistics": self.availability_logistics,
            "availability_mission": self.availability_mission,
            "cost": self.cost,
            "function_code": self.function_code,
            "hazard_rate_logistics": self.hazard_rate_logistics,
            "hazard_rate_mission": self.hazard_rate_mission,
            "level": self.level,
            "mmt": self.mmt,
            "mcmt": self.mcmt,
            "mpmt": self.mpmt,
            "mtbf_logistics": self.mtbf_logistics,
            "mtbf_mission": self.mtbf_mission,
            "mttr": self.mttr,
            "name": self.name,
            "parent_id": self.parent_id,
            "remarks": self.remarks,
            "safety_critical": self.safety_critical,
            "total_mode_count": self.total_mode_count,
            "total_part_count": self.total_part_count,
            "type_id": self.type_id,
        }

        return _attributes
