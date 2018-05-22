#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_rtkloadhistory.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKLoadHistory module algorithms and models."""

import pytest

from rtk.dao.RTKLoadHistory import RTKLoadHistory

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {'history_id': 1, 'description': 'Load History Description'}


@pytest.mark.integration
def test_rtkloadhistory_create(test_common_dao):
    """ __init__() should create an RTKLoadHistory model."""
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKLoadHistory).first()

    assert isinstance(DUT, RTKLoadHistory)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_load_history'
    assert DUT.history_id == 1
    assert DUT.description == 'Cycle Counts'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a dict of attribute:value pairs. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKLoadHistory).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['history_id'] == 1
    assert _attributes['description'] == 'Cycle Counts'


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKLoadHistory).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKLoadHistory {0:d} "
                    "attributes.".format(DUT.history_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key."""
    _session = test_common_dao.RTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKLoadHistory).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RTKLoadHistory.set_attributes().")

    ATTRIBUTES['description'] = 'Load History Description'
