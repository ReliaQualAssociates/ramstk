# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkdesignelectric.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing RAMSTKDesignElectric module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKDesignElectric

ATTRIBUTES = {
    'voltage_ac_operating': 0.0,
    'frequency_operating': 0.0,
    'type_id': 0,
    'resistance': 0.0,
    'package_id': 0,
    'technology_id': 0,
    'n_cycles': 0,
    'n_circuit_planes': 1,
    'contact_gauge': 0,
    'current_operating': 0.0,
    'n_hand_soldered': 0,
    'contact_rating_id': 0,
    'area': 0.0,
    'contact_form_id': 0,
    'years_in_production': 1,
    'n_active_pins': 0,
    'capacitance': 0.0,
    'temperature_case': 0.0,
    'current_rated': 0.0,
    'power_operating': 0.0,
    'configuration_id': 0,
    'temperature_hot_spot': 0.0,
    'temperature_junction': 0.0,
    'current_ratio': 0.0,
    'insulation_id': 0,
    'construction_id': 0,
    'insert_id': 0,
    'theta_jc': 0.0,
    'voltage_dc_operating': 0.0,
    'power_ratio': 0.0,
    'family_id': 0,
    'overstress': 0,
    'voltage_rated': 0.0,
    'feature_size': 0.0,
    'operating_life': 0.0,
    'application_id': 0,
    'weight': 0.0,
    'temperature_rated_max': 0.0,
    'voltage_ratio': 0.0,
    'temperature_rated_min': 0.0,
    'power_rated': 0.0,
    'environment_active_id': 0,
    'specification_id': 0,
    'matching_id': 0,
    'n_elements': 0,
    'environment_dormant_id': 0,
    'reason': '',
    'voltage_esd': 0.0,
    'manufacturing_id': 0,
    'n_wave_soldered': 0,
    'temperature_knee': 25.0,
    'temperature_rise': 0.0,
    'temperature_active': 35.0,
    'temperature_dormant': 25.0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKDesignElectric():
    """Class for testing the RAMSTKDesignElectric model."""
    @pytest.mark.integration
    def test_ramstkdesignelectric_create(self, test_program_dao):
        """ __init__() should create an RAMSTKDesignElectric model. """
        DUT = test_program_dao.session.query(RAMSTKDesignElectric).first()

        assert isinstance(DUT, RAMSTKDesignElectric)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_design_electric'
        assert DUT.hardware_id == 1
        assert DUT.application_id == 0
        assert DUT.area == 0.0
        assert DUT.capacitance == 0.0
        assert DUT.configuration_id == 0
        assert DUT.construction_id == 0
        assert DUT.contact_form_id == 0
        assert DUT.contact_gauge == 0
        assert DUT.contact_rating_id == 0
        assert DUT.current_operating == 0.0
        assert DUT.current_rated == 0.0
        assert DUT.current_ratio == 0.0
        assert DUT.environment_active_id == 0
        assert DUT.environment_dormant_id == 0
        assert DUT.family_id == 0
        assert DUT.feature_size == 0.0
        assert DUT.frequency_operating == 0.0
        assert DUT.insert_id == 0
        assert DUT.insulation_id == 0
        assert DUT.manufacturing_id == 0
        assert DUT.matching_id == 0
        assert DUT.n_active_pins == 0
        assert DUT.n_circuit_planes == 1
        assert DUT.n_cycles == 0
        assert DUT.n_elements == 0
        assert DUT.n_hand_soldered == 0
        assert DUT.n_wave_soldered == 0
        assert DUT.operating_life == 0.0
        assert DUT.overstress == 0
        assert DUT.package_id == 0
        assert DUT.power_operating == 0.0
        assert DUT.power_rated == 0.0
        assert DUT.power_ratio == 0.0
        assert DUT.reason == b''
        assert DUT.resistance == 0.0
        assert DUT.specification_id == 0
        assert DUT.technology_id == 0
        assert DUT.temperature_active == 35.0
        assert DUT.temperature_case == 0.0
        assert DUT.temperature_dormant == 25.0
        assert DUT.temperature_hot_spot == 0.0
        assert DUT.temperature_junction == 0.0
        assert DUT.temperature_rated_max == 0.0
        assert DUT.temperature_rated_min == 0.0
        assert DUT.temperature_rise == 0.0
        assert DUT.theta_jc == 0.0
        assert DUT.type_id == 0
        assert DUT.voltage_ac_operating == 0.0
        assert DUT.voltage_dc_operating == 0.0
        assert DUT.voltage_esd == 0.0
        assert DUT.voltage_rated == 0.0
        assert DUT.voltage_ratio == 0.0
        assert DUT.weight == 0.0
        assert DUT.years_in_production == 1

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a tuple of attribute values. """
        DUT = test_program_dao.session.query(RAMSTKDesignElectric).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes['voltage_ac_operating'] == 0.0
        assert _attributes['frequency_operating'] == 0.0
        assert _attributes['type_id'] == 0
        assert _attributes['resistance'] == 0.0
        assert _attributes['package_id'] == 0
        assert _attributes['technology_id'] == 0
        assert _attributes['n_cycles'] == 0
        assert _attributes['n_circuit_planes'] == 1
        assert _attributes['contact_gauge'] == 0
        assert _attributes['current_operating'] == 0.0
        assert _attributes['n_hand_soldered'] == 0
        assert _attributes['contact_rating_id'] == 0
        assert _attributes['area'] == 0.0
        assert _attributes['contact_form_id'] == 0
        assert _attributes['years_in_production'] == 1
        assert _attributes['n_active_pins'] == 0
        assert _attributes['capacitance'] == 0.0
        assert _attributes['temperature_case'] == 0.0
        assert _attributes['current_rated'] == 0.0
        assert _attributes['power_operating'] == 0.0
        assert _attributes['configuration_id'] == 0
        assert _attributes['temperature_hot_spot'] == 0.0
        assert _attributes['temperature_junction'] == 0.0
        assert _attributes['current_ratio'] == 0.0
        assert _attributes['insulation_id'] == 0
        assert _attributes['construction_id'] == 0
        assert _attributes['insert_id'] == 0
        assert _attributes['theta_jc'] == 0.0
        assert _attributes['voltage_dc_operating'] == 0.0
        assert _attributes['power_ratio'] == 0.0
        assert _attributes['family_id'] == 0
        assert _attributes['overstress'] == 0
        assert _attributes['voltage_rated'] == 0.0
        assert _attributes['feature_size'] == 0.0
        assert _attributes['operating_life'] == 0.0
        assert _attributes['application_id'] == 0
        assert _attributes['weight'] == 0.0
        assert _attributes['temperature_rated_max'] == 0.0
        assert _attributes['voltage_ratio'] == 0.0
        assert _attributes['temperature_rated_min'] == 0.0
        assert _attributes['power_rated'] == 0.0
        assert _attributes['environment_active_id'] == 0
        assert _attributes['hardware_id'] == 1
        assert _attributes['specification_id'] == 0
        assert _attributes['matching_id'] == 0
        assert _attributes['n_elements'] == 0
        assert _attributes['environment_dormant_id'] == 0
        assert _attributes['reason'] == b''
        assert _attributes['voltage_esd'] == 0.0
        assert _attributes['manufacturing_id'] == 0
        assert _attributes['n_wave_soldered'] == 0
        assert _attributes['temperature_knee'] == 25.0
        assert _attributes['temperature_rise'] == 0.0
        assert _attributes['temperature_active'] == 35.0
        assert _attributes['temperature_dormant'] == 25.0

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKDesignElectric).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKDesignElectric).first()

        ATTRIBUTES['type_id'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['type_id'] == 0

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKDesignElectric).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
