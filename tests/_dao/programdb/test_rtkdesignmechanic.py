#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkdesignmechanic.py is part of The RTK
#       Project
#
# All rights reserved.
"""Test class for testing the RTKDesignMechanic module algorithms and models. """

import pytest

from rtk.dao.RTKDesignMechanic import RTKDesignMechanic

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'pressure_upstream': 0.0,
    'frequency_operating': 0.0,
    'surface_finish': 0.0,
    'friction': 0.0,
    'length_compressed': 0.0,
    'load_id': 0,
    'n_cycles': 0,
    'balance_id': 0,
    'lubrication_id': 0,
    'water_per_cent': 0.0,
    'misalignment_angle': 0.0,
    'type_id': 0,
    'rpm_design': 0.0,
    'pressure_downstream': 0.0,
    'diameter_coil': 0.0,
    'manufacturing_id': 0,
    'pressure_contact': 0.0,
    'meyer_hardness': 0.0,
    'rpm_operating': 0.0,
    'length_relaxed': 0.0,
    'impact_id': 0,
    'n_ten': 0,
    'material_id': 0,
    'technology_id': 0,
    'service_id': 0,
    'flow_design': 0.0,
    'application_id': 0,
    'diameter_wire': 0.0,
    'deflection': 0.0,
    'filter_size': 0.0,
    'diameter_inner': 0.0,
    'pressure_rated': 0.0,
    'hardware_id': 1,
    'altitude_operating': 0.0,
    'thickness': 0.0,
    'diameter_outer': 0.0,
    'n_elements': 0,
    'contact_pressure': 0.0,
    'particle_size': 0.0,
    'casing_id': 0,
    'viscosity_dynamic': 0.0,
    'viscosity_design': 0.0,
    'torque_id': 0,
    'leakage_allowable': 0.0,
    'offset': 0.0,
    'width_minimum': 0.0,
    'load_operating': 0.0,
    'spring_index': 0.0,
    'flow_operating': 0.0,
    'pressure_delta': 0.0,
    'length': 0.0,
    'load_design': 0.0,
    'clearance': 0.0
}


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.hardware
def test_rtkdesignmechanic_create(test_dao):
    """ __init__() should create an RTKDesignMechanic model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKDesignMechanic).first()

    assert isinstance(DUT, RTKDesignMechanic)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_design_mechanic'
    assert DUT.hardware_id == 1
    assert DUT.altitude_operating == 0.0
    assert DUT.application_id == 0
    assert DUT.balance_id == 0
    assert DUT.clearance == 0.0
    assert DUT.casing_id == 0
    assert DUT.contact_pressure == 0.0
    assert DUT.deflection == 0.0
    assert DUT.diameter_coil == 0.0
    assert DUT.diameter_inner == 0.0
    assert DUT.diameter_outer == 0.0
    assert DUT.diameter_wire == 0.0
    assert DUT.filter_size == 0.0
    assert DUT.flow_design == 0.0
    assert DUT.flow_operating == 0.0
    assert DUT.frequency_operating == 0.0
    assert DUT.friction == 0.0
    assert DUT.impact_id == 0
    assert DUT.leakage_allowable == 0.0
    assert DUT.length == 0.0
    assert DUT.length_compressed == 0.0
    assert DUT.length_relaxed == 0.0
    assert DUT.load_design == 0.0
    assert DUT.load_id == 0
    assert DUT.load_operating == 0.0
    assert DUT.lubrication_id == 0
    assert DUT.manufacturing_id == 0
    assert DUT.material_id == 0
    assert DUT.meyer_hardness == 0.0
    assert DUT.misalignment_angle == 0.0
    assert DUT.n_ten == 0
    assert DUT.n_cycles == 0
    assert DUT.n_elements == 0
    assert DUT.offset == 0.0
    assert DUT.particle_size == 0.0
    assert DUT.pressure_contact == 0.0
    assert DUT.pressure_delta == 0.0
    assert DUT.pressure_downstream == 0.0
    assert DUT.pressure_rated == 0.0
    assert DUT.pressure_upstream == 0.0
    assert DUT.rpm_design == 0.0
    assert DUT.rpm_operating == 0.0
    assert DUT.service_id == 0
    assert DUT.spring_index == 0.0
    assert DUT.surface_finish == 0.0
    assert DUT.technology_id == 0
    assert DUT.thickness == 0.0
    assert DUT.torque_id == 0
    assert DUT.type_id == 0
    assert DUT.viscosity_design == 0.0
    assert DUT.viscosity_dynamic == 0.0
    assert DUT.water_per_cent == 0.0
    assert DUT.width_minimum == 0.0


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.hardware
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKDesignMechanic).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.hardware
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKDesignMechanic).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKDesignMechanic {0:d} "
                    "attributes.".format(DUT.hardware_id))


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.hardware
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKDesignMechanic).first()

    ATTRIBUTES.pop('length')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'length' in attribute "
                    "dictionary passed to RTKDesignMechanic.set_attributes().")

    ATTRIBUTES['length'] = 0.0
