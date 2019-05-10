#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkdesignelectric.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing RAMSTKDesignElectric module algorithms and models. """

import pytest

from ramstk.dao.programdb.RAMSTKDesignElectric import RAMSTKDesignElectric

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

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
    'hardware_id': 1,
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


@pytest.mark.integration
def test_ramstkdesignelectric_create(test_dao):
    """ __init__() should create an RAMSTKDesignElectric model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKDesignElectric).first()

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
    assert DUT.reason == ''
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
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKDesignElectric).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKDesignElectric).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKDesignElectric {0:d} "
                    "attributes.".format(DUT.hardware_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKDesignElectric).first()

    ATTRIBUTES.pop('family_id')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'family_id' in attribute "
                    "dictionary passed to RAMSTKDesignElectric.set_attributes().")

    ATTRIBUTES['family_id'] = 0
