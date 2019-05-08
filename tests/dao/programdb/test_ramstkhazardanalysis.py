#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkhazardanalysis.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing RAMSTKHazardAnalysis module algorithms and models."""

import pytest

from ramstk.dao.programdb.RAMSTKHazardAnalysis import RAMSTKHazardAnalysis

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'user_blob_3': b'',
    'user_blob_2': b'',
    'user_blob_1': b'',
    'system_severity': 'Medium',
    'result_2': 0.0,
    'result_3': 0.0,
    'assembly_probability': 'Level A - Frequent',
    'system_probability': 'Level A - Frequent',
    'system_probability_f': 'Level A - Frequent',
    'assembly_hri': 20,
    'system_hri': 20,
    'system_effect': '',
    'user_int_1': 0,
    'user_float_3': 0.0,
    'result_4': 0.0,
    'user_float_1': 0.0,
    'potential_hazard': '',
    'remarks': b'',
    'hazard_id': 1,
    'system_hri_f': 20,
    'result_5': 0.0,
    'assembly_severity': 'Medium',
    'assembly_probability_f': 'Level A - Frequent',
    'assembly_hri_f': 4,
    'assembly_effect': '',
    'function_4': '',
    'potential_cause': '',
    'system_mitigation': b'',
    'hardware_id': 1,
    'function_3': '',
    'function_2': '',
    'function_1': '',
    'user_int_3': 0,
    'user_int_2': 0,
    'assembly_severity_f': 'Medium',
    'system_severity_f': 'Medium',
    'assembly_mitigation': b'',
    'function_5': '',
    'result_1': 0.0,
    'user_float_2': 0.0
}


@pytest.mark.integration
def test_ramstkallocation_create(test_dao):
    """__init__() should create an RAMSTKHazardAnalysis model."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHazardAnalysis).first()

    assert isinstance(DUT, RAMSTKHazardAnalysis)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_hazard_analysis'
    assert DUT.revision_id == 1
    assert DUT.hardware_id == 1
    assert DUT.hazard_id == 1
    assert DUT.potential_hazard == ''
    assert DUT.potential_cause == ''
    assert DUT.assembly_effect == ''
    assert DUT.assembly_severity == 'Major'
    assert DUT.assembly_probability == 'Level A - Frequent'
    assert DUT.assembly_hri == 20
    assert DUT.assembly_mitigation == b''
    assert DUT.assembly_severity_f == 'Major'
    assert DUT.assembly_probability_f == 'Level A - Frequent'
    assert DUT.assembly_hri_f == 20
    assert DUT.function_1 == ''
    assert DUT.function_2 == ''
    assert DUT.function_3 == ''
    assert DUT.function_4 == ''
    assert DUT.function_5 == ''
    assert DUT.remarks == b''
    assert DUT.result_1 == 0.0
    assert DUT.result_2 == 0.0
    assert DUT.result_3 == 0.0
    assert DUT.result_4 == 0.0
    assert DUT.result_5 == 0.0
    assert DUT.system_effect == ''
    assert DUT.system_severity == 'Major'
    assert DUT.system_probability == 'Level A - Frequent'
    assert DUT.system_hri == 20
    assert DUT.system_mitigation == b''
    assert DUT.system_severity_f == 'Major'
    assert DUT.system_probability_f == 'Level A - Frequent'
    assert DUT.system_hri_f == 20
    assert DUT.user_blob_1 == b''
    assert DUT.user_blob_2 == b''
    assert DUT.user_blob_3 == b''
    assert DUT.user_float_1 == 0.0
    assert DUT.user_float_2 == 0.0
    assert DUT.user_float_3 == 0.0
    assert DUT.user_int_1 == 0
    assert DUT.user_int_2 == 0
    assert DUT.user_int_3 == 0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """get_attributes() should return a dict of attribute values."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHazardAnalysis).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['revision_id'] == 1
    assert _attributes['hardware_id'] == 1
    assert _attributes['hazard_id'] == 1
    assert _attributes['potential_hazard'] == ''
    assert _attributes['potential_cause'] == ''
    assert _attributes['assembly_effect'] == ''
    assert _attributes['assembly_severity'] == 'Major'
    assert _attributes['assembly_probability'] == 'Level A - Frequent'
    assert _attributes['assembly_hri'] == 20
    assert _attributes['assembly_mitigation'] == b''
    assert _attributes['assembly_severity_f'] == 'Major'
    assert _attributes['assembly_probability_f'] == 'Level A - Frequent'
    assert _attributes['assembly_hri_f'] == 20
    assert _attributes['function_1'] == ''
    assert _attributes['function_2'] == ''
    assert _attributes['function_3'] == ''
    assert _attributes['function_4'] == ''
    assert _attributes['function_5'] == ''
    assert _attributes['remarks'] == b''
    assert _attributes['result_1'] == 0.0
    assert _attributes['result_2'] == 0.0
    assert _attributes['result_3'] == 0.0
    assert _attributes['result_4'] == 0.0
    assert _attributes['result_5'] == 0.0
    assert _attributes['system_effect'] == ''
    assert _attributes['system_severity'] == 'Major'
    assert _attributes['system_probability'] == 'Level A - Frequent'
    assert _attributes['system_hri'] == 20
    assert _attributes['system_mitigation'] == b''
    assert _attributes['system_severity_f'] == 'Major'
    assert _attributes['system_probability_f'] == 'Level A - Frequent'
    assert _attributes['system_hri_f'] == 20
    assert _attributes['user_blob_1'] == b''
    assert _attributes['user_blob_2'] == b''
    assert _attributes['user_blob_3'] == b''
    assert _attributes['user_float_1'] == 0.0
    assert _attributes['user_float_2'] == 0.0
    assert _attributes['user_float_3'] == 0.0
    assert _attributes['user_int_1'] == 0
    assert _attributes['user_int_2'] == 0
    assert _attributes['user_int_3'] == 0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """set_attributes() should return a zero error code on success."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHazardAnalysis).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKHazardAnalysis 1 attributes.")


@pytest.mark.integration
def test_set_attributes_too_few_passed(test_dao):
    """set_attributes() should return a 40 error code when passed a dict with missing attributes."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHazardAnalysis).first()

    _error_code, _msg = DUT.set_attributes({
        'user_blob_3':
        '',
        'user_blob_2':
        '',
        'user_blob_1':
        '',
        'system_severity':
        'Medium',
        'result_2':
        0.0,
        'result_3':
        0.0,
        'assembly_probability':
        'Level A - Frequent',
        'system_probability':
        'Level A - Frequent',
        'system_probability_f':
        'Level A - Frequent',
        'assembly_hri':
        20,
        'system_hri':
        20,
        'system_effect':
        '',
        'user_int_1':
        0,
        'user_float_3':
        0.0,
        'result_4':
        0.0,
        'user_float_1':
        0.0,
        'potential_hazard':
        '',
        'remarks':
        '',
        'hazard_id':
        1,
        'system_hri_f':
        20,
        'result_5':
        0.0,
        'assembly_severity':
        'Medium',
        'assembly_probability_f':
        'Level A - Frequent',
        'assembly_hri_f':
        4,
        'assembly_effect':
        '',
        'function_4':
        '',
        'potential_cause':
        '',
        'system_mitigation':
        '',
        'hardware_id':
        1,
        'function_3':
        '',
        'function_2':
        '',
        'function_1':
        '',
        'user_int_3':
        0,
        'user_int_2':
        0,
        'assembly_severity_f':
        'Medium',
        'system_severity_f':
        'Medium',
        'assembly_mitigation':
        '',
        'function_5':
        '',
        'result_1':
        0.0
    })

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'user_float_2' in attribute "
                    "dictionary passed to RAMSTKHazardAnalysis.set_attributes().")


@pytest.mark.integration
def test_calculate_hri(test_dao):
    """calculate() should return False on success."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHazardAnalysis).filter(
        RAMSTKHazardAnalysis.hardware_id == 2).all()[0]

    DUT.assembly_severity = 'Medium'
    DUT.assembly_probability = 'Level A - Frequent'
    DUT.assembly_severity_f = 'Slight'
    DUT.assembly_probability_f = 'Level C - Occasional'
    DUT.system_severity = 'Medium'
    DUT.system_probability = 'Level B - Reasonably Probable'
    DUT.system_severity_f = 'Low'
    DUT.system_probability_f = 'Level D - Remote'

    assert not DUT.calculate()
    assert DUT.assembly_hri == 20
    assert DUT.assembly_hri_f == 6
    assert DUT.system_hri == 16
    assert DUT.system_hri_f == 6


@pytest.mark.integration
def test_calculate_user_defined(test_dao):
    """calculate() should return False when calculating user-defined risks."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKHazardAnalysis).filter(
        RAMSTKHazardAnalysis.hardware_id == 2).all()[0]

    DUT.assembly_severity = 'Medium'
    DUT.assembly_probability = 'Level A - Frequent'
    DUT.assembly_severity_f = 'Slight'
    DUT.assembly_probability_f = 'Level C - Occasional'
    DUT.system_severity = 'Medium'
    DUT.system_probability = 'Level B - Reasonably Probable'
    DUT.system_severity_f = 'Low'
    DUT.system_probability_f = 'Level D - Remote'
    DUT.user_float_1 = 4.4
    DUT.user_float_2 = 6.0
    DUT.user_int_1 = 2
    DUT.function_1 = "(uf1 + ui1) / uf2"

    assert not DUT.calculate()
    assert DUT.result_1 == pytest.approx(1.06666667)
