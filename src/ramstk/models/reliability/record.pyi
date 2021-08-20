# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKReliabilityRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    add_adj_factor: Any
    availability_logistics: Any
    availability_mission: Any
    avail_log_variance: Any
    avail_mis_variance: Any
    failure_distribution_id: Any
    hazard_rate_active: Any
    hazard_rate_dormant: Any
    hazard_rate_logistics: Any
    hazard_rate_method_id: Any
    hazard_rate_mission: Any
    hazard_rate_model: Any
    hazard_rate_percent: Any
    hazard_rate_software: Any
    hazard_rate_specified: Any
    hazard_rate_type_id: Any
    hr_active_variance: Any
    hr_dormant_variance: Any
    hr_logistics_variance: Any
    hr_mission_variance: Any
    hr_specified_variance: Any
    lambda_b: Any
    location_parameter: Any
    mtbf_logistics: Any
    mtbf_mission: Any
    mtbf_specified: Any
    mtbf_logistics_variance: Any
    mtbf_mission_variance: Any
    mtbf_specified_variance: Any
    mult_adj_factor: Any
    quality_id: Any
    reliability_goal: Any
    reliability_goal_measure_id: Any
    reliability_logistics: Any
    reliability_mission: Any
    reliability_log_variance: Any
    reliability_miss_variance: Any
    scale_parameter: Any
    shape_parameter: Any
    survival_analysis_id: Any
    def get_attributes(self): ...
