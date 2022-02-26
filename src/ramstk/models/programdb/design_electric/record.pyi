# Standard Library Imports
from typing import Dict, List, Tuple, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import derating, stress
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord
from ramstk.views.gtk3 import _

def do_check_overstress(
    overstress: Dict[str, List[float]], stress_type: str, limits: Dict[str, List[float]]
) -> Tuple[int, str]: ...

class RAMSTKDesignElectricRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Union[float, int, str]]
    __tablename__: str
    __table_args__: Dict[str, bool]
    revision_id: int
    hardware_id: int
    application_id: int
    area: float
    capacitance: float
    configuration_id: int
    construction_id: int
    contact_form_id: int
    contact_gauge: float
    contact_rating_id: int
    current_operating: float
    current_rated: float
    current_ratio: float
    environment_active_id: int
    environment_dormant_id: int
    family_id: int
    feature_size: float
    frequency_operating: float
    insert_id: int
    insulation_id: int
    manufacturing_id: int
    matching_id: int
    n_active_pins: int
    n_circuit_planes: int
    n_cycles: int
    n_elements: int
    n_hand_soldered: int
    n_wave_soldered: int
    operating_life: float
    overstress: int
    package_id: int
    power_operating: float
    power_rated: float
    power_ratio: float
    reason: str
    resistance: float
    specification_id: int
    technology_id: int
    temperature_active: float
    temperature_case: float
    temperature_dormant: float
    temperature_hot_spot: float
    temperature_junction: float
    temperature_knee: float
    temperature_rated_max: float
    temperature_rated_min: float
    temperature_rise: float
    theta_jc: float
    type_id: int
    voltage_ac_operating: float
    voltage_dc_operating: float
    voltage_esd: float
    voltage_rated: float
    voltage_ratio: float
    weight: float
    years_in_production: int
    def get_attributes(self) -> Dict[str, Union[float, int, str]]: ...
    def do_calculate_current_ratio(self) -> None: ...
    def do_calculate_power_ratio(self) -> None: ...
    def do_calculate_voltage_ratio(self) -> None: ...
    def do_derating_analysis(self, stress_limits: List[float]) -> None: ...
    def do_stress_analysis(self, category_id: int) -> None: ...
