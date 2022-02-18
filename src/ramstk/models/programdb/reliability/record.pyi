# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.analyses import dormancy
from ramstk.analyses.milhdbk217f import milhdbk217f
from ramstk.analyses.statistics import exponential, lognormal, normal, weibull
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKReliabilityRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Union[float, int, str]]
    __tablename__: str
    __table_args__: Dict[str, bool]
    revision_id: int
    hardware_id: int
    add_adj_factor: float
    availability_logistics: float
    availability_mission: float
    avail_log_variance: float
    avail_mis_variance: float
    failure_distribution_id: int
    hazard_rate_active: float
    hazard_rate_dormant: float
    hazard_rate_logistics: float
    hazard_rate_method_id: int
    hazard_rate_mission: float
    hazard_rate_model: str
    hazard_rate_percent: float
    hazard_rate_software: float
    hazard_rate_specified: float
    hazard_rate_type_id: int
    hr_active_variance: float
    hr_dormant_variance: float
    hr_logistics_variance: float
    hr_mission_variance: float
    hr_specified_variance: float
    lambda_b: float
    location_parameter: float
    mtbf_logistics: float
    mtbf_mission: float
    mtbf_specified: float
    mtbf_logistics_variance: float
    mtbf_mission_variance: float
    mtbf_specified_variance: float
    mult_adj_factor: float
    quality_id: int
    reliability_goal: float
    reliability_goal_measure_id: int
    reliability_logistics: float
    reliability_mission: float
    reliability_log_variance: float
    reliability_miss_variance: float
    scale_parameter: float
    shape_parameter: float
    survival_analysis_id: int
    def get_attributes(self) -> Dict[str, Union[float, int, str]]: ...
    def do_calculate_hazard_rate_active(
        self,
        multiplier: float,
        attributes: Dict[str, Union[float, int, str]],
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
    def do_calculate_mtbf(self, multiplier: float) -> None: ...
    def do_calculate_reliability(self, time: float, multiplier: float) -> None: ...
    def do_predict_active_hazard_rate(
        self, attributes: Dict[str, Union[float, int, str]]
    ) -> None: ...
