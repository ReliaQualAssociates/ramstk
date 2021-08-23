# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.analyses.statistics import (
    do_calculate_beta_bounds as do_calculate_beta_bounds,
)
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKValidationRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    validation_id: Any
    acceptable_maximum: Any
    acceptable_mean: Any
    acceptable_minimum: Any
    acceptable_variance: Any
    confidence: Any
    cost_average: Any
    cost_ll: Any
    cost_maximum: Any
    cost_mean: Any
    cost_minimum: Any
    cost_ul: Any
    cost_variance: Any
    date_end: Any
    date_start: Any
    description: Any
    measurement_unit: Any
    name: Any
    status: Any
    task_specification: Any
    task_type: Any
    time_average: Any
    time_ll: Any
    time_maximum: Any
    time_mean: Any
    time_minimum: Any
    time_ul: Any
    time_variance: Any
    def get_attributes(self): ...
    def calculate_task_time(self) -> None: ...
    def calculate_task_cost(self) -> None: ...
