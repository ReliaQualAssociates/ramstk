# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import derating, stress
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

def do_check_overstress(
    overstress: Dict[str, List[float]], stress_type: str
) -> Tuple[bool, str]: ...

class RAMSTKDesignElectricRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    application_id: Any
    area: Any
    capacitance: Any
    configuration_id: Any
    construction_id: Any
    contact_form_id: Any
    contact_gauge: Any
    contact_rating_id: Any
    current_operating: Any
    current_rated: Any
    current_ratio: Any
    environment_active_id: Any
    environment_dormant_id: Any
    family_id: Any
    feature_size: Any
    frequency_operating: Any
    insert_id: Any
    insulation_id: Any
    manufacturing_id: Any
    matching_id: Any
    n_active_pins: Any
    n_circuit_planes: Any
    n_cycles: Any
    n_elements: Any
    n_hand_soldered: Any
    n_wave_soldered: Any
    operating_life: Any
    overstress: Any
    package_id: Any
    power_operating: Any
    power_rated: Any
    power_ratio: Any
    reason: Any
    resistance: Any
    specification_id: Any
    technology_id: Any
    temperature_active: Any
    temperature_case: Any
    temperature_dormant: Any
    temperature_hot_spot: Any
    temperature_junction: Any
    temperature_knee: Any
    temperature_rated_max: Any
    temperature_rated_min: Any
    temperature_rise: Any
    theta_jc: Any
    type_id: Any
    voltage_ac_operating: Any
    voltage_dc_operating: Any
    voltage_esd: Any
    voltage_rated: Any
    voltage_ratio: Any
    weight: Any
    years_in_production: Any
    def get_attributes(self) -> Dict[str, Any]: ...
    def do_calculate_current_ratio(self) -> None: ...
    def do_calculate_power_ratio(self) -> None: ...
    def do_calculate_voltage_ratio(self) -> None: ...
    def do_derating_analysis(self, stress_limits: List[float]) -> None: ...
    def do_stress_analysis(self, category_id: int) -> None: ...
