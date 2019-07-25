# -*- coding: utf-8 -*-
#
#       tests.dao.progrmdb.test_ramstkprogramstatus.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKProgramStatus module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.dao.programdb.RAMSTKProgramStatus import RAMSTKProgramStatus

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'cost_remaining': 0.0,
    'date_status': date.today(),
    'time_remaining': 0.0,
    'revision_id': 1,
    'status_id': 1
}


@pytest.mark.integration
def test_ramstkprogramstatus_create(test_dao):
    """ __init__() should create an RAMSTKProgramStatus model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKProgramStatus).first()

    assert isinstance(DUT, RAMSTKProgramStatus)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_program_status'
    assert DUT.revision_id == 1
    assert DUT.status_id == 1
    assert DUT.cost_remaining == 0.0
    assert DUT.date_status == date.today()
    assert DUT.time_remaining == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute values. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKProgramStatus).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKProgramStatus).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKProgramStatus {0:d} "
                    "attributes.".format(DUT.revision_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKProgramStatus).first()

    ATTRIBUTES.pop('time_remaining')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'time_remaining' in "
                    "attribute dictionary passed to "
                    "RAMSTKProgramStatus.set_attributes().")

    ATTRIBUTES['time_remaining'] = 0.0
