# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKDesignMechanicRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    altitude_operating: Any
    application_id: Any
    balance_id: Any
    clearance: Any
    casing_id: Any
    contact_pressure: Any
    deflection: Any
    diameter_coil: Any
    diameter_inner: Any
    diameter_outer: Any
    diameter_wire: Any
    filter_size: Any
    flow_design: Any
    flow_operating: Any
    frequency_operating: Any
    friction: Any
    impact_id: Any
    leakage_allowable: Any
    length: Any
    length_compressed: Any
    length_relaxed: Any
    load_design: Any
    load_id: Any
    load_operating: Any
    lubrication_id: Any
    manufacturing_id: Any
    material_id: Any
    meyer_hardness: Any
    misalignment_angle: Any
    n_ten: Any
    n_cycles: Any
    n_elements: Any
    offset: Any
    particle_size: Any
    pressure_contact: Any
    pressure_delta: Any
    pressure_downstream: Any
    pressure_rated: Any
    pressure_upstream: Any
    rpm_design: Any
    rpm_operating: Any
    service_id: Any
    spring_index: Any
    surface_finish: Any
    technology_id: Any
    thickness: Any
    torque_id: Any
    type_id: Any
    viscosity_design: Any
    viscosity_dynamic: Any
    water_per_cent: Any
    width_minimum: Any
    def get_attributes(self): ...
