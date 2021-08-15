# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKHardware


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "alt_part_number": "",
        "attachments": "",
        "cage_code": "",
        "category_id": 0,
        "comp_ref_des": "S1",
        "cost": 0.0,
        "cost_failure": 0.0,
        "cost_hour": 0.0,
        "cost_type_id": 2,
        "description": "Test System",
        "duty_cycle": 100.0,
        "figure_number": "",
        "lcn": "",
        "level": 0,
        "manufacturer_id": 0,
        "mission_time": 100.0,
        "name": "",
        "nsn": "",
        "page_number": "",
        "parent_id": 0,
        "part": 0,
        "part_number": "",
        "quantity": 1,
        "ref_des": "S1",
        "remarks": "",
        "repairable": 0,
        "specification_number": "",
        "subcategory_id": 0,
        "tagged_part": 0,
        "total_cost": 0.0,
        "total_part_count": 0,
        "total_power_dissipation": 0.0,
        "year_of_manufacture": 2019,
    }


@pytest.fixture()
def mock_program_dao(monkeypatch):
    _hardware_1 = RAMSTKHardware()
    _hardware_1.revision_id = 1
    _hardware_1.hardware_id = 1
    _hardware_1.alt_part_number = ""
    _hardware_1.attachments = ""
    _hardware_1.cage_code = ""
    _hardware_1.category_id = 0
    _hardware_1.comp_ref_des = "S1"
    _hardware_1.cost = 0.0
    _hardware_1.cost_failure = 0.0
    _hardware_1.cost_hour = 0.0
    _hardware_1.cost_type_id = 2
    _hardware_1.description = "Test System"
    _hardware_1.duty_cycle = 100.0
    _hardware_1.figure_number = ""
    _hardware_1.lcn = ""
    _hardware_1.level = 0
    _hardware_1.manufacturer_id = 0
    _hardware_1.mission_time = 100.0
    _hardware_1.name = ""
    _hardware_1.nsn = ""
    _hardware_1.page_number = ""
    _hardware_1.parent_id = 0
    _hardware_1.part = 0
    _hardware_1.part_number = ""
    _hardware_1.quantity = 1
    _hardware_1.ref_des = "S1"
    _hardware_1.remarks = ""
    _hardware_1.repairable = 0
    _hardware_1.specification_number = ""
    _hardware_1.subcategory_id = 0
    _hardware_1.tagged_part = 0
    _hardware_1.total_cost = 0.0
    _hardware_1.total_part_count = 0
    _hardware_1.total_power_dissipation = 0.0
    _hardware_1.year_of_manufacture = 2019

    _hardware_2 = RAMSTKHardware()
    _hardware_2.revision_id = 1
    _hardware_2.hardware_id = 2
    _hardware_2.alt_part_number = ""
    _hardware_2.attachments = ""
    _hardware_2.cage_code = ""
    _hardware_2.category_id = 0
    _hardware_2.comp_ref_des = "S1:SS1"
    _hardware_2.cost = 0.0
    _hardware_2.cost_failure = 0.0
    _hardware_2.cost_hour = 0.0
    _hardware_2.cost_type_id = 2
    _hardware_2.description = "Test Sub-System"
    _hardware_2.duty_cycle = 100.0
    _hardware_2.figure_number = ""
    _hardware_2.lcn = ""
    _hardware_2.level = 0
    _hardware_2.manufacturer_id = 0
    _hardware_2.mission_time = 100.0
    _hardware_2.name = ""
    _hardware_2.nsn = ""
    _hardware_2.page_number = ""
    _hardware_2.parent_id = 1
    _hardware_2.part = 0
    _hardware_2.part_number = ""
    _hardware_2.quantity = 1
    _hardware_2.ref_des = "SS1"
    _hardware_2.remarks = ""
    _hardware_2.repairable = 0
    _hardware_2.specification_number = ""
    _hardware_2.subcategory_id = 0
    _hardware_2.tagged_part = 0
    _hardware_2.total_cost = 0.0
    _hardware_2.total_part_count = 0
    _hardware_2.total_power_dissipation = 0.0
    _hardware_2.year_of_manufacture = 2019

    _hardware_3 = RAMSTKHardware()
    _hardware_3.revision_id = 1
    _hardware_3.hardware_id = 3
    _hardware_3.alt_part_number = ""
    _hardware_3.attachments = ""
    _hardware_3.cage_code = ""
    _hardware_3.category_id = 0
    _hardware_3.comp_ref_des = "S1:SS1:A1"
    _hardware_3.cost = 0.0
    _hardware_3.cost_failure = 0.0
    _hardware_3.cost_hour = 0.0
    _hardware_3.cost_type_id = 2
    _hardware_3.description = "Test Assembly"
    _hardware_3.duty_cycle = 100.0
    _hardware_3.figure_number = ""
    _hardware_3.lcn = ""
    _hardware_3.level = 0
    _hardware_3.manufacturer_id = 0
    _hardware_3.mission_time = 100.0
    _hardware_3.name = ""
    _hardware_3.nsn = ""
    _hardware_3.page_number = ""
    _hardware_3.parent_id = 2
    _hardware_3.part = 0
    _hardware_3.part_number = ""
    _hardware_3.quantity = 1
    _hardware_3.ref_des = "A1"
    _hardware_3.remarks = ""
    _hardware_3.repairable = 0
    _hardware_3.specification_number = ""
    _hardware_3.subcategory_id = 0
    _hardware_3.tagged_part = 0
    _hardware_3.total_cost = 0.0
    _hardware_3.total_part_count = 0
    _hardware_3.total_power_dissipation = 0.0
    _hardware_3.year_of_manufacture = 2019

    DAO = MockDAO()
    DAO.table = [
        _hardware_1,
        _hardware_2,
        _hardware_3,
    ]

    yield DAO
