#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkmissionphase.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKPhase module algorithms and models."""

import pytest

from ramstk.dao.programdb.RAMSTKMissionPhase import RAMSTKMissionPhase

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'description': b'Test Mission Phase 1',
    'phase_end': 0.0,
    'phase_start': 0.0,
    'mission_id': 1,
    'phase_id': 1,
    'name': ''
}


@pytest.mark.integration
def test_ramstkmissionphase_create(test_dao):
    """ __init__() should create an RAMSTKPhase model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMissionPhase).first()

    assert isinstance(DUT, RAMSTKMissionPhase)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_mission_phase'
    assert DUT.mission_id == 1
    assert DUT.phase_id == 1
    assert DUT.description == b'Test Mission Phase 1'
    assert DUT.name == ''
    assert DUT.phase_start == 0.0
    assert DUT.phase_end == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMissionPhase).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMissionPhase).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKMissionPhase {0:d} "
                    "attributes.".format(DUT.phase_id))


@pytest.mark.integration
def test_set_attributes_wrong_type(test_dao):
    """ set_attributes() should return a 10 error code when passed the wrong data type. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMissionPhase).first()

    ATTRIBUTES.pop('phase_end')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'phase_end' in attribute "
                    "dictionary passed to RAMSTKMissionPhase.set_attributes().")
