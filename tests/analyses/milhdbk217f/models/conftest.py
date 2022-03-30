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
def test_attributes_fuse():
    yield {
        "category_id": 10,
        "subcategory_id": 3,
        "environment_active_id": 1,
        "piE": 1.0,
    }


@pytest.fixture
def test_attributes_inductor():
    yield {
        "category_id": 5,
        "subcategory_id": 1,
        "environment_active_id": 3,
        "insulation_id": 3,
        "family_id": 1,
        "construction_id": 1,
        "specification_id": 1,
        "quality_id": 1,
        "page_number": 3,
        "area": 12.5,
        "weight": 0.612,
        "power_operating": 0.875,
        "voltage_dc_operating": 3.3,
        "current_operating": 0.00108778877888,
        "temperature_active": 43.2,
        "piE": 5.0,
        "lambda_b": 0.0,
    }


@pytest.fixture
def test_attributes_integrated_circuit():
    yield {
        "category_id": 1,
        "subcategory_id": 1,
        "application_id": 2,
        "area": 0.5,
        "environment_active_id": 3,
        "family_id": 2,
        "feature_size": 0.8,
        "manufacturing_id": 1,
        "n_elements": 100,
        "n_active_pins": 32,
        "package_id": 1,
        "power_operating": 0.038,
        "technology_id": 1,
        "temperature_case": 48.3,
        "theta_jc": 125,
        "type_id": 1,
        "voltage_esd": 2000,
        "years_in_production": 3,
        "piE": 1.0,
        "piQ": 2.0,
    }


@pytest.fixture
def test_attributes_lamp():
    yield {
        "category_id": 10,
        "subcategory_id": 4,
        "environment_active_id": 3,
        "application_id": 1,
        "duty_cycle": 75.0,
        "voltage_rated": 12.0,
        "piE": 1.0,
    }


@pytest.fixture
def test_attributes_meter():
    yield {
        "category_id": 9,
        "subcategory_id": 1,
        "environment_active_id": 4,
        "type_id": 2,
        "application_id": 2,
        "temperature_active": 32.0,
        "temperature_rated_max": 85.0,
        "power_operating": 4.2,
        "piQ": 1.0,
        "piE": 7.0,
    }


@pytest.fixture
def test_attributes_relay():
    yield {
        "category_id": 6,
        "subcategory_id": 1,
        "environment_active_id": 3,
        "quality_id": 1,
        "type_id": 3,
        "technology_id": 2,
        "current_ratio": 0.38,
        "contact_rating_id": 2,
        "construction_id": 1,
        "application_id": 1,
        "contact_form_id": 1,
        "temperature_active": 38.2,
        "temperature_rated_max": 0.0,
        "n_cycles": 58,
        "piQ": 1.0,
    }


@pytest.fixture
def test_attributes_resistor():
    yield {
        "category_id": 3,
        "subcategory_id": 1,
        "environment_active_id": 3,
        "specification_id": 1,
        "family_id": 2,
        "construction_id": 1,
        "type_id": 2,
        "resistance": 22000,
        "n_elements": 3,
        "power_ratio": 0.45,
        "voltage_ratio": 0.86,
        "temperature_active": 37.6,
        "piQ": 2.0,
        "piE": 1.0,
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


@pytest.fixture
def test_attributes_switch():
    yield {
        "category_id": 7,
        "subcategory_id": 1,
        "environment_active_id": 3,
        "construction_id": 1,
        "quality_id": 1,
        "application_id": 1,
        "contact_form_id": 2,
        "n_elements": 8,
        "current_ratio": 0.45,
        "n_cycles": 2.3,
        "piE": 2.0,
        "piQ": 1.3,
    }
