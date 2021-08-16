# Third Party Imports
import pytest
from mocks import MockDAO

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKDesignElectric


@pytest.fixture(scope="function")
def test_attributes():
    yield {
        "revision_id": 1,
        "hardware_id": 1,
        "application_id": 0,
        "area": 0.0,
        "capacitance": 0.0,
        "configuration_id": 0,
        "construction_id": 0,
        "contact_form_id": 0,
        "contact_gauge": 0,
        "contact_rating_id": 0,
        "current_operating": 0.0,
        "current_rated": 0.0,
        "current_ratio": 0.0,
        "environment_active_id": 0,
        "environment_dormant_id": 0,
        "family_id": 0,
        "feature_size": 0.0,
        "frequency_operating": 0.0,
        "insert_id": 0,
        "insulation_id": 0,
        "manufacturing_id": 0,
        "matching_id": 0,
        "n_active_pins": 0,
        "n_circuit_planes": 1,
        "n_cycles": 0,
        "n_elements": 0,
        "n_hand_soldered": 0,
        "n_wave_soldered": 0,
        "operating_life": 0.0,
        "overstress": 0,
        "package_id": 0,
        "power_operating": 0.0,
        "power_rated": 0.0,
        "power_ratio": 0.0,
        "reason": "",
        "resistance": 0.0,
        "specification_id": 0,
        "technology_id": 0,
        "temperature_active": 35.0,
        "temperature_case": 0.0,
        "temperature_dormant": 25.0,
        "temperature_hot_spot": 0.0,
        "temperature_junction": 0.0,
        "temperature_knee": 25.0,
        "temperature_rated_max": 0.0,
        "temperature_rated_min": 0.0,
        "temperature_rise": 0.0,
        "theta_jc": 0.0,
        "type_id": 0,
        "voltage_ac_operating": 0.0,
        "voltage_dc_operating": 0.0,
        "voltage_esd": 0.0,
        "voltage_rated": 0.0,
        "voltage_ratio": 0.0,
        "weight": 0.0,
        "years_in_production": 1,
    }


@pytest.fixture()
def mock_program_dao(monkeypatch):
    _design_electric_1 = RAMSTKDesignElectric()
    _design_electric_1.revision_id = 1
    _design_electric_1.hardware_id = 1
    _design_electric_1.application_id = 0
    _design_electric_1.area = 0.0
    _design_electric_1.capacitance = 0.0
    _design_electric_1.configuration_id = 0
    _design_electric_1.construction_id = 0
    _design_electric_1.contact_form_id = 0
    _design_electric_1.contact_gauge = 0
    _design_electric_1.contact_rating_id = 0
    _design_electric_1.current_operating = 0.0
    _design_electric_1.current_rated = 0.0
    _design_electric_1.current_ratio = 0.0
    _design_electric_1.environment_active_id = 0
    _design_electric_1.environment_dormant_id = 0
    _design_electric_1.family_id = 0
    _design_electric_1.feature_size = 0.0
    _design_electric_1.frequency_operating = 0.0
    _design_electric_1.insert_id = 0
    _design_electric_1.insulation_id = 0
    _design_electric_1.manufacturing_id = 0
    _design_electric_1.matching_id = 0
    _design_electric_1.n_active_pins = 0
    _design_electric_1.n_circuit_planes = 1
    _design_electric_1.n_cycles = 0
    _design_electric_1.n_elements = 0
    _design_electric_1.n_hand_soldered = 0
    _design_electric_1.n_wave_soldered = 0
    _design_electric_1.operating_life = 0.0
    _design_electric_1.overstress = 0
    _design_electric_1.package_id = 0
    _design_electric_1.power_operating = 0.0
    _design_electric_1.power_rated = 0.0
    _design_electric_1.power_ratio = 0.0
    _design_electric_1.reason = ""
    _design_electric_1.resistance = 0.0
    _design_electric_1.specification_id = 0
    _design_electric_1.technology_id = 0
    _design_electric_1.temperature_active = 35.0
    _design_electric_1.temperature_case = 0.0
    _design_electric_1.temperature_dormant = 25.0
    _design_electric_1.temperature_hot_spot = 0.0
    _design_electric_1.temperature_junction = 0.0
    _design_electric_1.temperature_knee = 25.0
    _design_electric_1.temperature_rated_max = 0.0
    _design_electric_1.temperature_rated_min = 0.0
    _design_electric_1.temperature_rise = 0.0
    _design_electric_1.theta_jc = 0.0
    _design_electric_1.type_id = 0
    _design_electric_1.voltage_ac_operating = 0.0
    _design_electric_1.voltage_dc_operating = 0.0
    _design_electric_1.voltage_esd = 0.0
    _design_electric_1.voltage_rated = 0.0
    _design_electric_1.voltage_ratio = 0.0
    _design_electric_1.weight = 0.0
    _design_electric_1.years_in_production = 1

    _design_electric_2 = RAMSTKDesignElectric()
    _design_electric_2.revision_id = 1
    _design_electric_2.hardware_id = 2
    _design_electric_2.application_id = 0
    _design_electric_2.area = 0.0
    _design_electric_2.capacitance = 0.0
    _design_electric_2.configuration_id = 0
    _design_electric_2.construction_id = 0
    _design_electric_2.contact_form_id = 0
    _design_electric_2.contact_gauge = 0
    _design_electric_2.contact_rating_id = 0
    _design_electric_2.current_operating = 0.0
    _design_electric_2.current_rated = 0.0
    _design_electric_2.current_ratio = 0.0
    _design_electric_2.environment_active_id = 0
    _design_electric_2.environment_dormant_id = 0
    _design_electric_2.family_id = 0
    _design_electric_2.feature_size = 0.0
    _design_electric_2.frequency_operating = 0.0
    _design_electric_2.insert_id = 0
    _design_electric_2.insulation_id = 0
    _design_electric_2.manufacturing_id = 0
    _design_electric_2.matching_id = 0
    _design_electric_2.n_active_pins = 0
    _design_electric_2.n_circuit_planes = 1
    _design_electric_2.n_cycles = 0
    _design_electric_2.n_elements = 0
    _design_electric_2.n_hand_soldered = 0
    _design_electric_2.n_wave_soldered = 0
    _design_electric_2.operating_life = 0.0
    _design_electric_2.overstress = 0
    _design_electric_2.package_id = 0
    _design_electric_2.power_operating = 0.0
    _design_electric_2.power_rated = 0.0
    _design_electric_2.power_ratio = 0.0
    _design_electric_2.reason = ""
    _design_electric_2.resistance = 0.0
    _design_electric_2.specification_id = 0
    _design_electric_2.technology_id = 0
    _design_electric_2.temperature_active = 35.0
    _design_electric_2.temperature_case = 0.0
    _design_electric_2.temperature_dormant = 25.0
    _design_electric_2.temperature_hot_spot = 0.0
    _design_electric_2.temperature_junction = 0.0
    _design_electric_2.temperature_knee = 25.0
    _design_electric_2.temperature_rated_max = 0.0
    _design_electric_2.temperature_rated_min = 0.0
    _design_electric_2.temperature_rise = 0.0
    _design_electric_2.theta_jc = 0.0
    _design_electric_2.type_id = 0
    _design_electric_2.voltage_ac_operating = 0.0
    _design_electric_2.voltage_dc_operating = 0.0
    _design_electric_2.voltage_esd = 0.0
    _design_electric_2.voltage_rated = 0.0
    _design_electric_2.voltage_ratio = 0.0
    _design_electric_2.weight = 0.0
    _design_electric_2.years_in_production = 1

    _design_electric_3 = RAMSTKDesignElectric()
    _design_electric_3.revision_id = 1
    _design_electric_3.hardware_id = 3
    _design_electric_3.application_id = 0
    _design_electric_3.area = 0.0
    _design_electric_3.capacitance = 0.0
    _design_electric_3.configuration_id = 0
    _design_electric_3.construction_id = 0
    _design_electric_3.contact_form_id = 0
    _design_electric_3.contact_gauge = 0
    _design_electric_3.contact_rating_id = 0
    _design_electric_3.current_operating = 0.0
    _design_electric_3.current_rated = 0.0
    _design_electric_3.current_ratio = 0.0
    _design_electric_3.environment_active_id = 0
    _design_electric_3.environment_dormant_id = 0
    _design_electric_3.family_id = 0
    _design_electric_3.feature_size = 0.0
    _design_electric_3.frequency_operating = 0.0
    _design_electric_3.insert_id = 0
    _design_electric_3.insulation_id = 0
    _design_electric_3.manufacturing_id = 0
    _design_electric_3.matching_id = 0
    _design_electric_3.n_active_pins = 0
    _design_electric_3.n_circuit_planes = 1
    _design_electric_3.n_cycles = 0
    _design_electric_3.n_elements = 0
    _design_electric_3.n_hand_soldered = 0
    _design_electric_3.n_wave_soldered = 0
    _design_electric_3.operating_life = 0.0
    _design_electric_3.overstress = 0
    _design_electric_3.package_id = 0
    _design_electric_3.power_operating = 0.0
    _design_electric_3.power_rated = 0.0
    _design_electric_3.power_ratio = 0.0
    _design_electric_3.reason = ""
    _design_electric_3.resistance = 0.0
    _design_electric_3.specification_id = 0
    _design_electric_3.technology_id = 0
    _design_electric_3.temperature_active = 35.0
    _design_electric_3.temperature_case = 0.0
    _design_electric_3.temperature_dormant = 25.0
    _design_electric_3.temperature_hot_spot = 0.0
    _design_electric_3.temperature_junction = 0.0
    _design_electric_3.temperature_knee = 25.0
    _design_electric_3.temperature_rated_max = 0.0
    _design_electric_3.temperature_rated_min = 0.0
    _design_electric_3.temperature_rise = 0.0
    _design_electric_3.theta_jc = 0.0
    _design_electric_3.type_id = 0
    _design_electric_3.voltage_ac_operating = 0.0
    _design_electric_3.voltage_dc_operating = 0.0
    _design_electric_3.voltage_esd = 0.0
    _design_electric_3.voltage_rated = 0.0
    _design_electric_3.voltage_ratio = 0.0
    _design_electric_3.weight = 0.0
    _design_electric_3.years_in_production = 1

    DAO = MockDAO()
    DAO.table = [
        _design_electric_1,
        _design_electric_2,
        _design_electric_3,
    ]

    yield DAO
