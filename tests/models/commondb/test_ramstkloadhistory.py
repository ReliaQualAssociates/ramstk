#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_ramstkloadhistory.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKLoadHistory module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKLoadHistory

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {'history_id': 1, 'description': 'Load History Description'}


@pytest.mark.integration
def test_ramstkloadhistory_create(test_common_dao):
    """ __init__() should create an RAMSTKLoadHistory model."""
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKLoadHistory).first()

    assert isinstance(DUT, RAMSTKLoadHistory)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_load_history'
    assert DUT.history_id == 1
    assert DUT.description == 'Cycle Counts'


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a dict of attribute:value pairs. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKLoadHistory).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['history_id'] == 1
    assert _attributes['description'] == 'Cycle Counts'


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKLoadHistory).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKLoadHistory {0:d} "
                    "attributes.".format(DUT.history_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key."""
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKLoadHistory).first()

    ATTRIBUTES.pop('description')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'description' in attribute "
                    "dictionary passed to RAMSTKLoadHistory.set_attributes().")

    ATTRIBUTES['description'] = 'Load History Description'
