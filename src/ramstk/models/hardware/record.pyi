# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKHardwareRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    hardware_id: Any
    alt_part_number: Any
    attachments: Any
    cage_code: Any
    category_id: Any
    comp_ref_des: Any
    cost: Any
    cost_failure: Any
    cost_hour: Any
    cost_type_id: Any
    description: Any
    duty_cycle: Any
    figure_number: Any
    lcn: Any
    level: Any
    manufacturer_id: Any
    mission_time: Any
    name: Any
    nsn: Any
    page_number: Any
    parent_id: Any
    part: Any
    part_number: Any
    quantity: Any
    ref_des: Any
    remarks: Any
    repairable: Any
    specification_number: Any
    subcategory_id: Any
    tagged_part: Any
    total_cost: Any
    total_part_count: Any
    total_power_dissipation: Any
    year_of_manufacture: Any
    allocation: Any
    sia: Any
    reliability: Any
    milhdbkf: Any
    nswc: Any
    design_electric: Any
    design_mechanic: Any
    def get_attributes(self): ...
