# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKRevision(MockRAMSTKBaseRecord):
    __defaults__ = {
        "availability_logistics": 1.0,
        "availability_mission": 1.0,
        "cost": 0.0,
        "cost_failure": 0.0,
        "cost_hour": 0.0,
        "hazard_rate_active": 0.0,
        "hazard_rate_dormant": 0.0,
        "hazard_rate_logistics": 0.0,
        "hazard_rate_mission": 0.0,
        "hazard_rate_software": 0.0,
        "mmt": 0.0,
        "mcmt": 0.0,
        "mpmt": 0.0,
        "mtbf_logistics": 0.0,
        "mtbf_mission": 0.0,
        "mttr": 0.0,
        "name": "",
        "reliability_logistics": 1.0,
        "reliability_mission": 1.0,
        "remarks": "",
        "total_part_count": 1,
        "revision_code": "",
        "program_time": 0.0,
        "program_time_sd": 0.0,
        "program_cost": 0.0,
        "program_cost_sd": 0.0,
    }

    def __init__(self):
        self.revision_id = 0
        self.availability_logistics = self.__defaults__["availability_logistics"]
        self.availability_mission = self.__defaults__["availability_mission"]
        self.cost = self.__defaults__["cost"]
        self.cost_failure = self.__defaults__["cost_failure"]
        self.cost_hour = self.__defaults__["cost_hour"]
        self.hazard_rate_active = self.__defaults__["hazard_rate_active"]
        self.hazard_rate_dormant = self.__defaults__["hazard_rate_dormant"]
        self.hazard_rate_logistics = self.__defaults__["hazard_rate_logistics"]
        self.hazard_rate_mission = self.__defaults__["hazard_rate_mission"]
        self.hazard_rate_software = self.__defaults__["hazard_rate_software"]
        self.mmt = self.__defaults__["mmt"]
        self.mcmt = self.__defaults__["mcmt"]
        self.mpmt = self.__defaults__["mpmt"]
        self.mtbf_logistics = self.__defaults__["mtbf_logistics"]
        self.mtbf_mission = self.__defaults__["mtbf_mission"]
        self.mttr = self.__defaults__["mttr"]
        self.name = self.__defaults__["name"]
        self.reliability_logistics = self.__defaults__["reliability_logistics"]
        self.reliability_mission = self.__defaults__["reliability_mission"]
        self.remarks = self.__defaults__["remarks"]
        self.total_part_count = self.__defaults__["total_part_count"]
        self.revision_code = self.__defaults__["revision_code"]
        self.program_time = self.__defaults__["program_time"]
        self.program_time_sd = self.__defaults__["program_time_sd"]
        self.program_cost = self.__defaults__["program_cost"]
        self.program_cost_sd = self.__defaults__["program_cost_sd"]

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "availability_logistics": self.availability_logistics,
            "availability_mission": self.availability_mission,
            "cost": self.cost,
            "cost_failure": self.cost_failure,
            "cost_hour": self.cost_hour,
            "hazard_rate_active": self.hazard_rate_active,
            "hazard_rate_dormant": self.hazard_rate_dormant,
            "hazard_rate_logistics": self.hazard_rate_logistics,
            "hazard_rate_mission": self.hazard_rate_mission,
            "hazard_rate_software": self.hazard_rate_software,
            "mmt": self.mmt,
            "mcmt": self.mcmt,
            "mpmt": self.mpmt,
            "mtbf_logistics": self.mtbf_logistics,
            "mtbf_mission": self.mtbf_mission,
            "mttr": self.mttr,
            "name": self.name,
            "reliability_logistics": self.reliability_logistics,
            "reliability_mission": self.reliability_mission,
            "remarks": self.remarks,
            "total_part_count": self.total_part_count,
            "revision_code": self.revision_code,
            "program_time": self.program_time,
            "program_time_sd": self.program_time_sd,
            "program_cost": self.program_cost,
            "program_cost_sd": self.program_cost_sd,
        }

        return _attributes
