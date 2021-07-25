# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.analyses.criticality import (
    calculate_mode_criticality as calculate_mode_criticality,
)
from ramstk.analyses.criticality import (
    calculate_mode_hazard_rate as calculate_mode_hazard_rate,
)
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager as RAMSTKAnalysisManager

class AnalysisManager(RAMSTKAnalysisManager):
    def __init__(
        self, configuration: RAMSTKUserConfiguration, **kwargs: Dict[str, Any]
    ) -> None: ...
    def _do_calculate_criticality(self, item_hr: float) -> None: ...
