#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkmechanism.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKMechanism module algorithms and models."""

import pytest

from ramstk.Utilities import OutOfRangeError
from ramstk.dao.programdb.RAMSTKMechanism import RAMSTKMechanism

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'rpn_new': 0,
    'rpn_occurrence_new': 0,
    'rpn_occurrence': 0,
    'mode_id': 1,
    'description': u'Test Failure Mechanism #1',
    'rpn_detection_new': 0,
    'rpn_detection': 0,
    'rpn': 0,
    'mechanism_id': 1,
    'pof_include': 1
}


@pytest.mark.integration
def test_ramstkmechanism_create(test_dao):
    """ __init__() should create an RAMSTKMechanism model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    assert isinstance(DUT, RAMSTKMechanism)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_mechanism'
    assert DUT.mode_id == 4
    assert DUT.mechanism_id == 1
    assert DUT.description == 'Test Failure Mechanism #1 for Mode ID 4'
    assert DUT.pof_include == 1
    assert DUT.rpn == 0
    assert DUT.rpn_detection == 0
    assert DUT.rpn_detection_new == 0
    assert DUT.rpn_new == 0
    assert DUT.rpn_occurrence == 0
    assert DUT.rpn_occurrence_new == 0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute:value pairs. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['mode_id'] == 4
    assert _attributes['mechanism_id'] == 1
    assert _attributes['description'] == ('Test Failure Mechanism #1 for Mode '
                                          'ID 4')
    assert _attributes['pof_include'] == 1
    assert _attributes['rpn'] == 0
    assert _attributes['rpn_detection'] == 0
    assert _attributes['rpn_detection_new'] == 0
    assert _attributes['rpn_new'] == 0
    assert _attributes['rpn_occurrence'] == 0
    assert _attributes['rpn_occurrence_new'] == 0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKMechanism 1 attributes.")


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RAMSTKMechanism.set_attributes().")

    ATTRIBUTES['description'] = 'Test Failure Mechanism #1'


@pytest.mark.integration
def test_calculate_rpn(test_dao):
    """ calculate_rpn() always returns a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    DUT.rpn_detection = 4
    DUT.rpn_detection_new = 3
    DUT.rpn_occurrence = 7
    DUT.rpn_occurrence_new = 5

    _error_code, _msg = DUT.calculate_rpn(7, 4)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Calculating failure mechanism {0:d} RPN.'. \
                         format(DUT.mechanism_id))
    assert DUT.rpn == 196
    assert DUT.rpn_new == 60


@pytest.mark.integration
def test_calculate_rpn_out_of_range_severity_inputs(test_dao):
    """ calculate_rpn() raises OutOfRangeError for 11 < severity inputs < 0. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    DUT.rpn_detection = 6
    DUT.rpn_detection_new = 4
    DUT.rpn_occurrence = 7
    DUT.rpn_occurrence_new = 5

    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(0, 1)
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(11, 1)
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 0)
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 11)


@pytest.mark.integration
def test_calculate_rpn_out_of_range_occurrence_inputs(test_dao):
    """ calculate_rpn() raises OutOfRangeError for 11 < occurrence inputs < 0."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    DUT.rpn_occurrence = 0
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 1)
    DUT.rpn_occurrence = 11
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 1)


@pytest.mark.integration
def test_calculate_rpn_out_of_range_new_occurrence_inputs(test_dao):
    """ calculate_rpn() raises OutOfRangeError for 11 < new occurrence inputs < 0. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    DUT.rpn_occurrence_new = 0
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 1)
    DUT.rpn_occurrence_new = 11
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 1)


@pytest.mark.integration
def test_calculate_rpn_out_of_range_detection_inputs(test_dao):
    """ calculate_rpn() raises OutOfRangeError for 11 < detection inputs < 0. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    DUT.rpn_detection = 0
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 10)
    DUT.rpn_detection = 11
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 10)


@pytest.mark.integration
def test_calculate_rpn_out_of_range_new_detection_inputs(test_dao):
    """ calculate_rpn() raises OutOfRangeError for 11 < new detection inputs < 0. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    DUT.rpn_detection_new = 0
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 10)
    DUT.rpn_detection_new = 11
    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(1, 10)


@pytest.mark.integration
def test_calculate_rpn_out_of_range_result(test_dao):
    """ calculate_rpn() returns a non-zero error code when the calculated RPN is outide the range (0, 1000]. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMechanism).first()

    DUT.rpn_detection = 12
    DUT.rpn_detection_new = 3
    DUT.rpn_occurrence = -7
    DUT.rpn_occurrence_new = 5

    with pytest.raises(OutOfRangeError):
        DUT.calculate_rpn(8, 4)
