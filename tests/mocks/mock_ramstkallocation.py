# RAMSTK Local Imports
from . import MockRAMSTKBaseRecord


class MockRAMSTKAllocation(MockRAMSTKBaseRecord):
    __defaults__ = {
        "availability_alloc": 0.0,
        "duty_cycle": 100.0,
        "env_factor": 1,
        "goal_measure_id": 1,
        "hazard_rate_alloc": 0.0,
        "hazard_rate_goal": 0.0,
        "included": 1,
        "int_factor": 1,
        "allocation_method_id": 1,
        "mission_time": 100.0,
        "mtbf_alloc": 0.0,
        "mtbf_goal": 0.0,
        "n_sub_systems": 1,
        "n_sub_elements": 1,
        "parent_id": 1,
        "percent_weight_factor": 0.0,
        "reliability_alloc": 1.0,
        "reliability_goal": 1.0,
        "op_time_factor": 1,
        "soa_factor": 1,
        "weight_factor": 1.0,
    }

    def __init__(self):
        self.revision_id = 0
        self.hardware_id = 0
        self.availability_alloc = self.__defaults__["availability_alloc"]
        self.duty_cycle = self.__defaults__["duty_cycle"]
        self.env_factor = 1
        self.goal_measure_id = 1
        self.hazard_rate_alloc = 0.0
        self.hazard_rate_goal = 0.0
        self.included = 1
        self.int_factor = 1
        self.allocation_method_id = 1
        self.mission_time = 100.0
        self.mtbf_alloc = 0.0
        self.mtbf_goal = 0.0
        self.n_sub_systems = 1
        self.n_sub_elements = 1
        self.parent_id = 1
        self.percent_weight_factor = 0.0
        self.reliability_alloc = 1.0
        self.reliability_goal = 1.0
        self.op_time_factor = 1
        self.soa_factor = 1
        self.weight_factor = 1.0

    def get_attributes(self):
        _attributes = {
            "revision_id": self.revision_id,
            "hardware_id": self.hardware_id,
            "availability_alloc": self.availability_alloc,
            "duty_cycle": self.duty_cycle,
            "env_factor": self.env_factor,
            "goal_measure_id": self.goal_measure_id,
            "hazard_rate_alloc": self.hazard_rate_alloc,
            "hazard_rate_goal": self.hazard_rate_goal,
            "included": self.included,
            "int_factor": self.int_factor,
            "allocation_method_id": self.allocation_method_id,
            "mission_time": self.mission_time,
            "mtbf_alloc": self.mtbf_alloc,
            "mtbf_goal": self.mtbf_goal,
            "n_sub_systems": self.n_sub_systems,
            "n_sub_elements": self.n_sub_elements,
            "parent_id": self.parent_id,
            "percent_weight_factor": self.percent_weight_factor,
            "reliability_alloc": self.reliability_alloc,
            "reliability_goal": self.reliability_goal,
            "op_time_factor": self.op_time_factor,
            "soa_factor": self.soa_factor,
            "weight_factor": self.weight_factor,
        }

        return _attributes
