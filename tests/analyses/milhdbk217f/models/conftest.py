# Third Party Imports
import pytest


@pytest.fixture
def test_attributes_capacitor():
    yield {
        "hardware_id": 12,
        "subcategory_id": 1,
        "temperature_rated_max": 105.0,
        "temperature_active": 45.0,
        "voltage_ratio": 0.54,
        "capacitance": 0.0000033,
        "construction_id": 1,
        "configuration_id": 1,
        "resistance": 0.05,
        "voltage_dc_operating": 3.3,
        "voltage_ac_operating": 0.04,
        "lambda_b": 0.0,
        "piQ": 1.0,
        "piE": 1.0,
        "piC": 0.0,
        "piCF": 0.0,
        "piCV": 0.0,
        "piSR": 0.0,
        "hazard_rate_active": 0.0,
    }


@pytest.fixture
def test_attributes_connection():
    yield {
        "category_id": 8,
        "subcategory_id": 1,
        "environment_active_id": 2,
        "type_id": 2,
        "specification_id": 1,
        "n_circuit_planes": 3,
        "contact_gauge": 20,
        "current_operating": 0.005,
        "n_active_pins": 15,
        "n_cycles": 0.1,
        "temperature_active": 40.0,
        "insert_id": 2,
        "n_wave_soldered": 45,
        "n_hand_soldered": 4,
        "lambda_b": 0.0,
        "piQ": 1.0,
        "piE": 1.0,
        "piC": 0.0,
        "piK": 0.0,
        "piP": 0.0,
        "hazard_rate_active": 0.0,
    }


@pytest.fixture
def test_attributes_crystal():
    yield {
        "category_id": 10,
        "subcategory_id": 1,
        "environment_active_id": 1,
        "frequency_operating": 10.0,
        "piE": 1.0,
        "piQ": 1.0,
    }


@pytest.fixture
def test_attributes_filter():
    yield {
        "category_id": 10,
        "subcategory_id": 2,
        "environment_active_id": 1,
        "type_id": 1,
        "piQ": 1.0,
        "piE": 4.0,
    }


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
