# Third Party Imports
import pytest


@pytest.fixture
def test_attributes_semiconductor():
    yield {
        "category_id": 2,
        "subcategory_id": 1,
        "environment_active_id": 3,
        "type_id": 1,
        "quality_id": 1,
        "application_id": 1,
        "package_id": 2,
        "construction_id": 1,
        "matching_id": 2,
        "duty_cycle": 65.0,
        "voltage_ratio": 0.45,
        "temperature_case": 38.2,
        "theta_jc": 15.0,
        "power_operating": 0.5,
        "frequency_operating": 2.5,
        "n_elements": 8,
        "power_rated": 1.0,
        "current_rated": 0.25,
        "current_operating": 0.038,
        "power_ratio": 0.28,
        "piE": 1.0,
    }
