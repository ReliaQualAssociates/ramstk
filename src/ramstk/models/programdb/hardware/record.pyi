# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKHardwareRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Dict[str, Union[float, int, str]]
    __tablename__: str
    __table_args__: UniqueConstraint
    revision_id: int
    hardware_id: int
    alt_part_number: str
    attachments: str
    cage_code: str
    category_id: int
    comp_ref_des: str
    cost: float
    cost_failure: float
    cost_hour: float
    cost_type_id: int
    description: str
    duty_cycle: float
    figure_number: str
    lcn: str
    level: int
    manufacturer_id: int
    mission_time: float
    name: str
    nsn: str
    page_number: str
    parent_id: int
    part: int
    part_number: str
    quantity: int
    ref_des: str
    remarks: str
    repairable: int
    specification_number: str
    subcategory_id: int
    tagged_part: int
    total_cost: float
    total_part_count: int
    total_power_dissipation: float
    year_of_manufacture: int
    allocation: relationship
    sia: relationship
    reliability: relationship
    milhdbkf: relationship
    nswc: relationship
    design_electric: relationship
    design_mechanic: relationship
    def get_attributes(self) -> Dict[str, Union[float, int, str]]: ...
    def do_calculate_total_cost(self) -> None: ...
