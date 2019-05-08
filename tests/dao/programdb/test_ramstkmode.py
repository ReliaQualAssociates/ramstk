#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests._dao.TestRAMSTKMode.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKMode module algorithms and models."""

import pytest

from ramstk.Utilities import OutOfRangeError
from ramstk.dao.programdb.RAMSTKMode import RAMSTKMode

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'mode_id': 1,
    'effect_local': '',
    'mission': 'Default Mission',
    'other_indications': '',
    'mode_criticality': 0.0,
    'single_point': 0,
    'design_provisions': b'',
    'type_id': 0,
    'rpn_severity_new': 1,
    'effect_next': '',
    'detection_method': '',
    'hardware_id': -1,
    'operator_actions': b'',
    'critical_item': 0,
    'hazard_rate_source': '',
    'severity_class': '',
    'description': 'Test Functional Failure Mode #1',
    'mission_phase': '',
    'mode_probability': '',
    'remarks': b'',
    'function_id': 1,
    'mode_ratio': 0.0,
    'mode_hazard_rate': 0.0,
    'rpn_severity': 1,
    'isolation_method': '',
    'effect_end': '',
    'mode_op_time': 0.0,
    'effect_probability': 0.0
}


@pytest.mark.integration
def test_ramstkmode_create(test_dao):
    """ __init__() should create an RAMSTKMode model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    assert isinstance(DUT, RAMSTKMode)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_mode'
    assert DUT.function_id == 1
    assert DUT.hardware_id == -1
    assert DUT.mode_id == 1
    assert DUT.critical_item == 0
    assert DUT.description == 'Test Functional Failure Mode #1'
    assert DUT.design_provisions == b''
    assert DUT.detection_method == ''
    assert DUT.effect_end == ''
    assert DUT.effect_local == ''
    assert DUT.effect_next == ''
    assert DUT.effect_probability == 0.0
    assert DUT.hazard_rate_source == ''
    assert DUT.isolation_method == ''
    assert DUT.mission == 'Default Mission'
    assert DUT.mission_phase == ''
    assert DUT.mode_criticality == 0.0
    assert DUT.mode_hazard_rate == 0.0
    assert DUT.mode_op_time == 0.0
    assert DUT.mode_probability == ''
    assert DUT.mode_ratio == 0.0
    assert DUT.operator_actions == b''
    assert DUT.other_indications == ''
    assert DUT.remarks == b''
    assert DUT.rpn_severity == 1
    assert DUT.rpn_severity_new == 1
    assert DUT.severity_class == ''
    assert DUT.single_point == 0
    assert DUT.type_id == 0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute name:value pairs. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKMode {0:d} "
                    "attributes.".format(DUT.hardware_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    ATTRIBUTES.pop('remarks')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'remarks' in attribute "
                    "dictionary passed to RAMSTKMode.set_attributes().")


@pytest.mark.integration
def test_calculate_criticality(test_dao):
    """ calculate_criticality() should return False on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    DUT.mode_ratio = 0.5
    DUT.mode_op_time = 5.8
    DUT.effect_probability = 0.43

    _error_code, _msg = DUT.calculate_criticality(0.0000563)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Calculating failure mode 1 criticality.")

    pytest.approx(DUT.mode_hazard_rate, 2.815e-05)
    pytest.approx(DUT.mode_criticality, 7.02061e-05)


@pytest.mark.integration
def test_calculate_criticality_out_of_range_hazard_rate_input(test_dao):
    """ calculate_criticality() raises OutOfRangeError for item_hr < 0.0. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    DUT.mode_ratio = 1.0
    DUT.mode_op_time = 1.0
    DUT.effect_probability = 1.0

    pytest.raises(OutOfRangeError, DUT.calculate_criticality, -0.000015)


@pytest.mark.integration
def test_calculate_criticality_out_of_range_ratio_input(test_dao):
    """ calculate_criticality() raises OutOfRangeError for 0.0 > ratio > 1.0. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    DUT.mode_ratio = -0.1
    DUT.mode_op_time = 1.0
    DUT.effect_probability = 1.0

    pytest.raises(OutOfRangeError, DUT.calculate_criticality, 1.1)


@pytest.mark.integration
def test_calculate_criticality_out_of_range_op_time_input(test_dao):
    """ calculate_criticality() raises OutOfRangeError for 0.0 > operating time. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    DUT.mode_ratio = 0.5
    DUT.mode_op_time = -1.2
    DUT.effect_probability = 1.0

    pytest.raises(OutOfRangeError, DUT.calculate_criticality, 1)


@pytest.mark.integration
def test_calculate_criticality_out_of_range_eff_prob_input(test_dao):
    """ calculate_criticality() raises OutOfRangeError for 0.0 <= effect probability =< 1.0. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    DUT.mode_ratio = 11.0
    DUT.mode_op_time = 1.0
    DUT.effect_probability = 2.3

    pytest.raises(OutOfRangeError, DUT.calculate_criticality, 1)


@pytest.mark.integration
def test_calculate_criticality_out_of_range_mode_hazard_rate(test_dao):
    """ calculate_criticality() raises OutOfRangeError for 0 > mode hazard rate. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    DUT.mode_ratio = -0.5
    DUT.mode_op_time = 1.0
    DUT.effect_probability = 1.0

    pytest.raises(OutOfRangeError, DUT.calculate_criticality, 1)


@pytest.mark.integration
def test_calculate_criticality_out_of_range_mode_criticality(test_dao):
    """ calculate_criticality() raises OutOfRangeError for 0 > mode criticality. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMode).first()

    DUT.mode_ratio = -0.5
    DUT.mode_op_time = 1.0
    DUT.effect_probability = 1.0

    pytest.raises(OutOfRangeError, DUT.calculate_criticality, 1)
