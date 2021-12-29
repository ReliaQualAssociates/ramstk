# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.analyses import dormancy
from ramstk.analyses.milhdbk217f import milhdbk217f
from ramstk.analyses.statistics import exponential, lognormal, normal, weibull
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
    def get_attributes(self) -> Dict[str, Any]: ...
    def do_calculate_hazard_rate_active(
        self,
        multiplier: float,
        attributes: Dict[str, Any],
        time: float = 1.0,
    ) -> None: ...
    def do_calculate_hazard_rate_dormant(
        self,
        category_id: int,
        subcategory_id: int,
        env_active: int,
        env_dormant: int,
    ) -> None: ...
    def do_calculate_hazard_rate_logistics(self) -> None: ...
    def do_calculate_hazard_rate_mission(self, duty_cycle: float) -> None: ...
    def do_calculate_mtbf(self) -> None: ...
    def do_calculate_reliability(self, time: float) -> None: ...
    def do_predict_active_hazard_rate(self, attributes: Dict[str, Any]) -> None: ...
