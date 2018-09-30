#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkmission.py is part of The RAMSTK Project
#
# All rights reserved.
""" Test class for testing the RAMSTKMission module algorithms and models. """

import pytest

from ramstk.dao.programdb.RAMSTKMission import RAMSTKMission

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'mission_id': 1,
    'revision_id': 1,
    'mission_time': 0.0,
    'description': 'Test Mission',
    'time_units': u'hours'
}


@pytest.mark.integration
def test_ramstkmission_create(test_dao):
    """ __init__() should create an RAMSTKMission model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMission).first()

    assert isinstance(DUT, RAMSTKMission)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_mission'
    assert DUT.revision_id == 1
    assert DUT.mission_id == 1
    assert DUT.description == 'Test Mission'
    assert DUT.mission_time == 0.0
    assert DUT.time_units == 'hours'


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMission).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMission).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKMission {0:d} "
                    "attributes.".format(DUT.mission_id))


@pytest.mark.integration
def test_set_attributes_too_few_passed(test_dao):
    """ set_attributes() should return a zero error code when passed too few attributes. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKMission).first()

    ATTRIBUTES.pop('time_units')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'time_units' in attribute "
                    "dictionary passed to RAMSTKMission.set_attributes().")
